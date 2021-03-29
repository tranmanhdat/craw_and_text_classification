# craw_and_text_classification
## About project  
 This project wil show how to crawl data from _Vietnamese_ newspaper web ([tuoitre](https://tuoitre.vn/))  and from
  that data, we will try to classify document into some category (such as
   sport, economic, business...)
## Setup to run  
   Ubuntu 18.04.5 LST, python 3.6.9
   run: pip install -r requirements.txt
## Crawl data  
```
python craw_data/crawl_new.py <folder_save> <number_page_to_crawl>  
python craw_data/crawl_special_dulich.py <folder_save> <number_page_to_crawl> 
python craw_data/crawl_special_congnghe.py <folder_save> <number_page_to_crawl> 
python craw_data/crawl_special_thethao.py <folder_save> <number_page_to_crawl> 
```
## Statistic data:
```
python classify_text/statistic_data.py <folder_data> <folder_save_fig>  
```
run take random to get random data from crawled data
```
 
python3 classify_text/1_take_random_data.py <folder_in> <folder_out>
```
then statistic again to check random

```
python classify_text/statistic_after_process.py <folder_data> <folder_save_fig>
```
## Preprocessing data
after take random, let change name folder data to data_1 to run below code
```
python classify_text/2_preprocess.py ../data_1 ../data_2
python classify_text/3_cal_freq.py ../data_2 freq_text
python classify_text/4_remove_stop_words.py ../data_2 ../data_4
python classify_text/5_split_train_test.py ../data_4 ../data_5
```
## Classify
```
python classify_text/6.1_Naive_Bayes_Classifier.py
python classify_text/6.2_svm.py
```
check my other repos to run classify with [VDCNN](https://github.com/tranmanhdat/text-classification-models-tf) and [Text-GCN](https://github.com/tranmanhdat/text_gcn)  
