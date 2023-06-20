# Extract and load data from pdf invoices with dlt and langchain
Here we create a simple dlt data source that downloads a list of PDF invoices from google drive and then uses [langchain](https://github.com/hwchase17/langchain) to get interesting information like recipient name or total amount from it. The data source is then plugged into dlt pipeline that loads the data to duckdb. At the end you can launch a Streamlit app that will show you a few reports.

> 💡 This is a PoC that current with current state of the art LLMs you can extract meaningful information almost from any unstructured blob of data and then plug the dlt to export that information as data set.

# How to run
[**Watch the pipeline in action**](https://player.gotolstoy.com/onny9ql7upm13)

# How to customize
1. Change the drive folder id in `config.toml` to get documents from other places
2. Change the queries in [process_one_pdf_to_structured function](invoice_tracking_pipeline/invoice_tracking.py) to get more details on invoices or change them completely if you have other type of document
3. [Change the duckdb to bigquery](https://dlthub.com/docs/walkthroughs/share-a-dataset) to persist your data


# What's next: universal data sources
We want to build an universal data source that uses LLM to extract data from any binary or unstructured source: pdfs (like here), web pages from web scraping, images etc. Users just describes what they want using natural language, sends a blob of data, we use LLM to extract the data and then `dlt` is used to infer the data structure and load it to database. Looks cool, no? But we'll get there step by step.

1. We'll move this `pdf` source to (verified sources repo)[] and make it easy to customize the natural language queries. As usual it gets the user friendly credentials handling, incremental loads and all other goodies
2. We'll make document type pluggable. Not only PDFs but also html pages and other formats supported by langchain.
3. We'll experiment with [EVAPORATE-CODE](https://github.com/HazyResearch/evaporate) to generate Python code that extracts the desired information. It is really a waste of resources to use LLMs to do the work - use LLMs to write a tool that does the work.