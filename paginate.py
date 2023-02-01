from data import fetch_sales_data, count_of_data

def paginate(start, limit): 
    
    meta = {}
    total_records = count_of_data()
    meta["count"] = total_records
    
    if start>total_records:
        return dict({"message": "Start limit is greater than total_records"})
    
    elif start==1:
        data = fetch_sales_data(start, limit)
        meta["limit"] = limit
        meta["next"] = f'/mentorskool/v1/sales?start={start+limit}&limit={limit}'
        meta["previous"] = ""
        meta["data"] = data
    elif (start+limit)>=total_records:
        ## We are subtracting 1 from extra_demand because, as in case if start is 9819, and limit is 5 thus by calculation extra_demand 
        # is of 4 records but in actual extra_demand is of 3 records only as 9818 and 9819 are present.
        ## Ex:- If start=9819 and limit=5 then extra_demand=((9819+5) - (9819)) - 1 = (9823-9819)-1 = 3
        ## And then 3 will be subtracted from the limit, i.e 5-3=2 and thuw we will get the total_records that are 
        # 9818 and 9819
        extra_demand = ((start+limit)-(total_records)) - 1
        limit -= extra_demand
        data = fetch_sales_data(start, limit)
        meta["limit"] = limit
        meta["next"] = ""
        meta["previous"] = f'/mentorskool/v1/sales?start={start-limit}&limit={limit}'
        meta["data"] = data
    else:
        data = fetch_sales_data(start, limit)
        meta["limit"] = limit
        meta["next"] = f'/mentorskool/v1/sales?start={start+limit}&limit={limit}'
        if (start-limit)<0:
            meta["previous"] = f'/mentorskool/v1/sales?start={1}&limit={limit}'
        else:
            meta["previous"] = f'/mentorskool/v1/sales?start={start-limit}&limit={limit}'
        meta["data"] = data

    return meta

if __name__ == "__main__":
    meta = paginate(1, 100)
    print(meta)