import requests
import json
import time
import random
from dhooks import *
from datetime import datetime

webhook_url = ''###Your webhook
delay = '' #seconds

#Only monitor orange
#https://www.thenorthface.com/shop/mens-1996-retro-nuptse-jacket-nf0a3c8d?variationId=V0W

def post_message(instock):
	hook = Webhook(webhook_url)
	embed = Embed(
		description='',
		color=0x5CDBF0,
		timestamp='now'
		)
	embed.set_title(title="[ TNF ] -MEN'S 1996 RETRO NUPTSE JACKET",url='https://www.thenorthface.com/shop/mens-1996-retro-nuptse-jacket-nf0a3c8d?variationId=V0W')
	embed.add_field(name='**Stock:**',value='\n'.join(instock))
	embed.set_footer(text='dev. by @zyx898',icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg')
	embed.set_thumbnail('http://images.thenorthface.com/is/image/TheNorthFace/NF0A3C8D_V0W_hero')
	hook.send(embed=embed)

	print(str(datetime.now()) + ' Successfully Post to Discord ---------- [ The North Face ] -------------')



def parse_size_id_stock(r_json):
    size_ids = r_json['attributes']['7000000000000074622']
    size_id_list = []
    for i in size_ids:
        for size_id in i['catentryId']:
            size_id_list.append(str(i['display']) + '-' + str(size_id))
        
    size_id_stock_list = []
    stocks = r_json['stock']
    for stock_id in stocks:
        for size_id in size_id_list:
            if stock_id in size_id:
                size_id_stock_list.append(size_id + "-"+ str(r_json['stock'][stock_id]))
    return size_id_stock_list

def main():
    old_instock = []

    while True:
        url = 'https://www.thenorthface.com/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?langId=-1&storeId=7001&productId=723756&requestype=ajax&requesttype=ajax'

        headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}

        r = requests.get(url,headers=headers)
        r_json = json.loads(r.text)
        stock_list = parse_size_id_stock(r_json)

        color = r_json['attributes']['7000000000000074501'][8]['display']
        color_sizes = r_json['attributes']['7000000000000074501'][8]['catentryId']

        product_stocks = []
        instock = []
        for i in color_sizes:
            for c in stock_list:
                if str(i) in c:
                    stock = c.split('-')[0] +' - ' + c.split('-')[2]
                    product_stocks.append(stock)
        for i in product_stocks:
            if i.split(' - ')[1] == '0':
                pass
            else:
                instock.append(i.split(' - ')[0])


        if ''.join(old_instock) != ''.join(instock):
            post_message(instock)
            old_instock = instock
            print(str(datetime.now())+" Posted to Discord")
        else:
            print(str(datetime.now())+" Montioring TNF Site-------")
            time.sleep(int(delay))


main()
