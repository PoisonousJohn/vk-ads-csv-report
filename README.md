# vk-ads-csv-report
Get ad plans statistics reports and write it to csv

VK Ads API token is read from VK_ADS_TOKEN env variable

### Example usage

```
VK_ADS_TOKEN="your_token_here" python3 main.py -o output.csv
```

### Example output

```csv
name,date,clicks,shows,spent
test1,2023-05-24,561,33951,2209.63
test1,2023-05-25,719,36780,2275.05
test1,2023-05-26,799,34470,2228.91
```

### Full usage doc

```
usage: Simple vk ads report fetcher [-h] -o OUTPUT_FILE [--date_from DATE_FROM] [--date_to DATE_TO]
Simple vk ads report fetcher: error: the following arguments are required: -o/--output_file
```