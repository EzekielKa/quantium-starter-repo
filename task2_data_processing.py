data_files = ["data\daily_sales_data_0.csv", "data\daily_sales_data_1.csv", "data\daily_sales_data_2.csv"] 

with open("data/output.csv", "w") as output:
    output.write("sales,date,region\n")

    for files in data_files: 
            with open(files ,"r") as file:
                header = file.readline()
                headers = header.strip().split(",")

                for line in file: 
                    values = line.strip().split(",")
                    if values[0] == "" or values[1] == "":
                        continue
            
                    product = values[0]
                    price = float(values[1].replace("$", ""))
                    quantity = int(values[2])
                    date = values[3]
                    region = values[4]
                    sales = round(price  * quantity, 2) 

                    if product == "pink morsel":
                        output.write(f"{sales}, {date}, {region}\n")

