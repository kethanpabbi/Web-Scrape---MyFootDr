# MyFootDr Clinics Scraper (Wayback Machine)

This project scrapes **all MyFootDr clinic information** from the Wayback Machine and stores it in a clean, deduplicated CSV file.

It is designed to be:
- Resumable
- Idempotent (safe to re-run)
- Fault-tolerant
- Snapshot-aware

---

## Target Website

Wayback snapshot entry point:

https://web.archive.org/web/20250708180027/https://www.myfootdr.com.au/our-clinics/

The scraper:
1. Visits every **region**
2. Visits every **clinic within each region**
3. Extracts clinic data
4. Writes results to a CSV file

---

## Output

### CSV File
`myfootdr_clinics.csv`

### Columns (exact order)
```
Name of Clinic
Address
Email
Phone
Services
```

### Deduplication Key
Each clinic is uniquely identified by:
```
(Name of Clinic, Address)
```

Existing rows are **updated**, not duplicated.

---

## Files Generated

### `myfootdr_clinics.csv`
- Master dataset
- Continuously updated
- Safe to interrupt and resume

### `failed_regions.txt`
Contains region slugs that failed to load.

### `failed_clinics.txt`
Contains clinic URLs that failed to scrape.

---

## Snapshot Strategy

The Wayback Machine is inconsistent.  
Different pages exist in different snapshots.

### Default Snapshots
```
20250708180027
20250517063937
20250516141742
```

### Region-Specific Snapshots
Some regions require older captures:
```
victoria
western-australia
```

If one snapshot fails, the scraper automatically tries the next.

---

## Scraping Flow

1. Discover regions from `/our-clinics/`
2. Discover clinic URLs per region
3. Scrape each clinic page
4. Upsert results into CSV
5. Track failures for retry

---

## Field Extraction Rules

### Name
From:
```
#clinic-metacard-2020 h1.entry-title
```

### Address
From:
```
.clinic-metabox .address
```

### Email
From visible `mailto:` links  
Fallback: `NA`

### Phone
From:
- `tel:` links
- Visible numeric text  
Fallback: `NA`

### Services
Collected from:
- Bullet lists (`ul > li`)
- Service cards (`clinic-2020-services`)

Fallback: `NA`

---

## Retry Strategy

- Failed regions and clinics are written to text files
- Retry scripts reattempt only failed entries
- Successfully recovered entries are removed from failure lists

---

## Interrupt Safety

You can stop execution at any time.  
All progress is preserved automatically.

---

## Requirements

- Python 3.8+
- Libraries:
```
requests
beautifulsoup4
```

---

## Result

A complete, deduplicated dataset of all MyFootDr clinics, built robustly using the Wayback Machine.
