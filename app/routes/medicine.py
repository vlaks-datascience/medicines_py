import requests, json
import pandas as pd
from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.config.medicine import conn
from app.schemas.medicine import medicine_entity, medicines_entity, pricings_entity
from bs4 import BeautifulSoup


medicine_router = APIRouter()

@medicine_router.get('/api/crawler', status_code=200, tags=['Crawler API'])
async def get_medicines(SMCID: Optional[str] = None):
    if SMCID:
        if conn.vlaksbato.crawler_data.find_one({'smcid':SMCID}) == None:
            raise HTTPException(status_code=404, detail=f'There is no medicine with the id |{SMCID}| in the collection, or it is empty!')
        else:
            return medicine_entity(conn.vlaksbato.crawler_data.find_one({'smcid':SMCID}))
    else:
        return medicines_entity(conn.vlaksbato.crawler_data.find())


@medicine_router.post('/api/crawler/trigger', status_code=201, tags=['Crawler API'])
async def save_to_crawler_data_collection():
    page_count, result_count = get_page_result()
    if conn.vlaksbato.crawler_data.count_documents({}) == result_count:
        raise HTTPException(status_code=409, detail='Collection [crawler_data] already exists with the same data!')
    for i in range(1, page_count):
        source = requests.get(f'https://www.scottishmedicines.org.uk/umbraco/Api/ListMedicineAdviceApi/GetResultsByType?active-tab=0&node-id=6990&current-page-0={i}')
        soup = str(BeautifulSoup(r'''{}'''.format(source.text), 'html.parser')).replace('=\"\"','\'')
        json_object = json.loads(soup)
        for key in json_object['SearchResults']:
            medicine_object = {
                'smcid':key['DrugId'],
                'date':key['PublishedDateText'],
                'medicine':key['Heading'],
                'submission':key['SubmissionType'],
                'indication':key['Indication'][3:len(key['Indication'])-4],
                'link_to':'https://www.scottishmedicines.org.uk' + key['Link']['Url']
            }
            conn.vlaksbato.crawler_data.insert_one(dict(medicine_object))
    return f'Successfully fetched {result_count} medicines from https://www.scottishmedicines.org.uk/medicines-advice/'



@medicine_router.get('/api/pricing_data', status_code=200, tags=['Pricing Data API'])
async def get_pricing_data(MEDICINE_NAME: Optional[str] = None):
    if MEDICINE_NAME:
        if conn.vlaksbato.pricing_data.find_one({'medicine':MEDICINE_NAME}) == None:
            raise HTTPException(status_code=404, detail=f'There is no medicine with the name |{MEDICINE_NAME}| in the collection, or it is empty!')
        else:
            return pricings_entity(conn.vlaksbato.pricing_data.find({'medicine':MEDICINE_NAME}))
    else:
        return pricings_entity(conn.vlaksbato.pricing_data.find())


@medicine_router.post('/api/pricing_data/process', status_code=201, tags=['Pricing Data API'])
async def save_to_pricing_data_collection():
    if 'pricing_data' in conn.vlaksbato.list_collection_names():
        raise HTTPException(status_code=409, detail='Collection [pricing_data] already exists!') 
    df = pd.read_csv('app/pricing_data.csv', keep_default_na=False)
    data = df.to_dict('records')
    conn.vlaksbato.pricing_data.insert_many(data)
    return f'Fetched {df.shape[0]} objects from pricing_data excel!'


@medicine_router.get('/', tags=['Redirect tab'])
async def redirect():
    response = RedirectResponse(url='/docs')
    return response


### Additional function for getting PageCount and ResultCount
def get_page_result():
    source = requests.get('https://www.scottishmedicines.org.uk/umbraco/Api/ListMedicineAdviceApi/GetResultsByType?active-tab=0&node-id=6990&current-page-0=1')
    soup = str(BeautifulSoup(r'''{}'''.format(source.text), 'html.parser'))
    json_object = json.loads(soup)
    return json_object['PageCount']+1, json_object['ResultCount']
