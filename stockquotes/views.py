from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST["ticker_symbol"]

		api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_1c83ad666a554b26b58b7479f050d001")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error getting content..."
		return render(request, 'home.html', {"api": api})

	else:
		return render(request, 'home.html', {"ticker": "Enter ticker symbol in above search..."})

	

	
def add_stock(request):
	import requests
	import json
	if request.method == 'POST':
		form = StockForm(request.POST or None)
		
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added!"))
			return redirect('add_stock')
		else:
			messages.success(request, ("Please enter a stock"))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_1c83ad666a554b26b58b7479f050d001")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error getting content..."
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def about(request):
	my_first_name = 'Deepak'
	my_last_name = 'Awal'
	context = {'my_first_name': my_first_name, 'my_last_name': my_last_name}
	return render(request, 'about.html', context)


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted"))
	return redirect('delete_stock')



def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})