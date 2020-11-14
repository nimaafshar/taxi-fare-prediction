# New York City Taxi Fare Prediction

Training an ML model to predict Taxi Fares using Google BigQueryML and [NYC TLC Trips](https://console.cloud.google.com/marketplace/product/city-of-new-york/nyc-tlc-trips).

[NYC taxi fare prediction Kaggle Challenge](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/overview/getting-started)


## Experiment Details
This dataset is available on google cloud public datasets and it contains new york city's taxi and limousine trips since 2009.
in it's tables it usually contains filed like number of passangers, pickup and dropoff latitude and longitude, trip distance, fare amount, tax amount, tolls amount, payment information, tips , taxes , etc. we use [Google BigQuery](https://console.cloud.google.com/bigquery) to dive into the data and train a regression model on it. Google BigQuery is an standard SQL developed by google. and it allows us to explore and train on terabytes and terabytes of data with dealing with memory limits and operation headaches.

In this project we first loaded the dataset into the bigquery and decided to filter outliers by limiting the fare amount to 6-200 dollars and limiting the pickup and dropoff locations to newyork city itself in order to avoid very long cab trips in our train and evaulation set. these 2 decreased number of rows from 1 billion to 820 million rows. cause for this experiment we didn't want to use all the 820 million rows for training or evaluation, we used `FARM_FINGERPRINT` as hash function on `pickup_datetime` column and picked 1/1000 of data for training and another 1/1000 of data for evaluation. for feature engineering, we picked  `tolls_amount` + `fare_amount` to be the label for prediction (cause tips are considered noise in `total_fare`). we used day of week, hour of day, euclidean distance between pickup and dropoff point and distance between pickup and dropoff point in latitude and longitude and passengers count as our features. cause Google BigQuery is pretty new it only supports Linear Regression models from all types of regression models. thus we used linear regression as our model. after that we calculated RMSE as evaluation metric and it was about 5 . thus the model could predict fare amount with 5 dollar accuracy wich is not bad for such a small training set and simple model. we can reach better accuracy with training on more data, filtering more outliers, using normalization on some features and picking more complex models.

## How to Execute
1. select your project from [here](https://console.cloud.google.com/projectselector2/home/dashboard).

2. Enable the bigquery API from [here](https://console.cloud.google.com/flows/enableapi?apiid=bigquery)

3. Set up Authentication
    - Goto [Service Account Key Page](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
    - From the **Service account list**, select New service account.
    - In the **Service account name** field, enter a name.
    - From the Role list, select **Project > Owner**.
    - Click **Create**. A JSON file that contains your key downloads to your computer.
    - Rename the downloaded JSON file to `service_key.json` and place it into the project root.

4. Activate the python virtualenv (recommended)

    in project root:
    ```bash
    source venv/bin/activate
    ```
Or intall requirement packages from `requirements.txt`

5. View data stats
    this query filter 200 million rows from total 1 billion rows of data as outliers
    based on fare amount and travel path. after that this shows row counts, minimum and maximum fares in the remaining rows
    and average and standard deviation of the fare amount. we should get as close as possible to this average and stddev
    in our prediction results
    ```bash
    python3 show_data_stats.py
    ```

6. Create a `taxi` dataset in your project to store models
    this will create a dataset named `taxi` in your project in order to put further BigQueryML models in it in the next steps
    ```bash
    python3 create_dataset.py
    ```

7. Create your model
    this query creates a linear regression model based on some columns of the new york cab data to predict total fare
    and uses 1/1000 of data as training set almost randomly. more description about the model is available at the next section
    ```bash
    python3 create_model.py
    ```

8. Evaulate your model
    this query evaluates with RMSE score (wich has the same unit as total fare).
    the lower the score is. the better your model is working.
    ```bash
    python3 evaluate_model.py
    ```
### Alternative Implementation

we can also implement taxifare-prediction model in google cloud using google AI platform and tensorflow models. cause we are using a simple `LinearRegression` model for fare prediction. we can use one of the ready-to-train model images. but in order to use them we should preprocess training and validation data to fit their special format. so we can use dataflow notebooks in order to preprocess the data. for example, one of the preprocessing steps is removing the first row (label row) from the CSV file. after make a training job with a linear regression model and out taxifare data, we should deploy the model. we deploy the model into the AI platform and connect it to API. we can also use this model in BigQuery. we insert model into our BigQuery dataset. but for using it we should convert needed data from every row of database table into a csv row and feed it into the model with a unique key for each row we predict at a time.
