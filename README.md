# DataScienceRentalPrice

## Description

The main goal of this project is to help on the rental process by estimating the total rent price of houses, apartments or studios. It is using real data collected from 5andar, a pretty famous rental site here in Brazil.

## Overview

* Scrapped around 14000 rental posts (in two chuncks) from 5andar using python.
* Removed duplicated and cleaned the data to make it usable to the model.
* Feature engineering and data analysis to find some patterns.
* Reduced input size data from 56 to 31 by using some feature selection.
* Created a final model with an 749 MAE (16% of error when comparing to the target mean value)

### Web Scrapping
Constructed a scrapper to collect most of the information contained on the 5andar rental posts, such as:

* Title
* Address
* Area
* Bedroom
* Garage
* Floor
* Pet
* Furniture
* Area
* Subway
* Rent
* Condominium
* Taxes
* Fire Insurance
* Services
* Total

### Data Cleaning

After the data was collected I did some cleaning to let it more usable for our model.   

* Merged the two parts of the extracted data and removed duplicates
* Removed rows with no total price, as it is the target value
* Extracted the rental type (house, apartment, studio) and district from the title column
* Removed unnecessary text from area, garage and floor
* Parsed bedroom and suite quantity from "bedroom" column
* Removed unnecessary text from all the "price" columns
