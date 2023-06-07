# vk-ads-csv-report
Get ad plans statistics reports and write it to csv

VK Ads API token is read from VK_ADS_TOKEN env variable

Important: this script uses a [New Vk Ads API](https://ads.vk.com/doc/api/info/%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B2%20API)

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