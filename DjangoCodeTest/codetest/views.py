from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
import requests
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)
# Create your views here.

pack_api_url = 'https://6466e9a7ba7110b663ab51f2.mockapi.io/api/v1/{0}/?customer_id={1}'

class CustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(write_only=True)

class FetchApiView(ModelViewSet):
    
    serializer_class = CustomerSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return None
    
    
    def create(self, request, *args, **kwargs):
        #response will be like this 
        '''
        Request Param : {
          "customer_id":102
        }

        Return:
        {
            "data": [
                {
                    "customer_id": 102,
                    "pack_data": [
                        {
                            "ingredient": "Tocopherol as Vitamin E Acetate",
                            "inventory_code": "VITET",
                            "quantity": 10.4,
                            "unit": "mg"
                        },
                        {
                            "ingredient": "Vitamin D as Ergocalciferol",
                            "inventory_code": "VITDE",
                            "quantity": 15,
                            "unit": "mcg"
                        }
                    ],
                    "id": "2"
                },
                {
                    "customer_id": 102,
                    "pack_data": [
                        {
                            "inventory_code": "PRCHLPF19",
                            "ingredient": "Lactobacillus paracasei F-19",
                            "quantity": 2,
                            "unit": "B cfu"
                        },
                        {
                            "inventory_code": "PRCHLC431",
                            "ingredient": "Lactobacillus casei 431",
                            "quantity": 20,
                            "unit": "B cfu"
                        }
                    ],
                    "id": "2"
                }
            ],
            "success": true
        }
        '''
        try:
            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            #check customer_id
            customer_id = serializer.validated_data.get('customer_id')
            
            logger.info(f'Requested customer id: {customer_id}')
            combine_data = list()
            pack_1 = requests.get(pack_api_url.format('pack1',customer_id))
            if pack_1.status_code==200:
                pack_1_res_data = pack_1.json()
                if pack_1_res_data and isinstance(pack_1_res_data,list):
                    combine_data+=pack_1_res_data
            pack_2 = requests.get(pack_api_url.format('pack2',customer_id))  
            if pack_2.status_code==200:
                pack_2_res_data = pack_2.json()
                if pack_2_res_data and isinstance(pack_2_res_data,list):
                    combine_data+=pack_2_res_data
            #log combine data
            logger.info(combine_data)
            
            return Response({
                "data":combine_data,
                "success":True
            })
        except ValidationError as ve:
            #log validation error 
            logger.error(ve.detail)
            return Response({
                "error":ve.detail,
                "success":False
            })
        except Exception as err:
            #log exception error
            logger.info(err)
            return Response({
                "error":"Something went wrong",
                "success":False
            })
        

 

    