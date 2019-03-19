from flask import Flask, jsonify, request
import boto3
import json
app = Flask(__name__)

@app.route("/", methods=['POST'])
def get_data():
	count = request.get_json(silent=True)['queryResult']['parameters']['count']
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('arduinoSensorData')
	unique = []
	#for i in range(1,20):
	response = table.scan()
	items = response['Items']
	#new_items= items.to_dataframe()
	#print(items)
	for i in items:
		unique.append(i['uuid'])
	unique = sorted(unique)
	print(unique[-1])	
	response = table.get_item(
		Key={
	        'uuid': unique[-1]})
	item_1 = response['Item']
	value = item_1['value']
	time = item_1['uuid']
	print(time, value)
	my_response = 'Total count is'+' '+str(value)
	reply = {
	"fulfillmentText": my_response,
        }
	return jsonify(reply) 

if __name__ == "__main__":
    app.run(debug=True)