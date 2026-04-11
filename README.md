# Movie-Recommendation-Platform-
Recommends movies to you


Unfortunatly it is not fully working as it being delayed and soem parts of the frontend and backend are just not working and 
coperating with each other 

and delays with aws learner becuase of the limited budget that is given 

to use first download the requirments file with 
pip install -r requirements.txt

then to run the backend use in the terminal
uvicorn main:app --reload

and the front end use
python -m http.server 5500


.env file incase needed for examination 

# Secret file the contains 

# this contains sensitive API credentials
# dont commit this file and keep it ignored

TmdbAccessToken=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMTI5NzhjMDJkYzA3Y2EyMDEyYzI4ODdjZDU0NzUwMCIsIm5iZiI6MTc3MzA1ODIzNS44NDYwMDAyLCJzdWIiOiI2OWFlYjhiYmFlOWYzMDFjMTRjMWU1ODYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.IFNSHpf40Bk14o9JnCNNwwfzKSu2PW2FnhHK3Deivs8

TmdbApiKey=b12978c02dc07ca2012c2887cd547500

#Url for TMDB API
TmdbUrl=https://api.themoviedb.org/3

DB_HOST = database-1.cs49ca45dmit.us-east-1.rds.amazonaws.com
DB_USER = admin

DB_PASS = E4Kxvk4TPuRDN8W

DB_NAME = final_project

#jwt secret
SECRET_KEY = jchdiaphducajhsucjsusdiseoejsmmslpfientnghudsmnmwksjnfdnekospwerufhndjpocbjs