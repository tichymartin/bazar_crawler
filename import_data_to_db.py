# from general import insert_keywords_to_db, insert_stopusers_to_db, insert_stopwords_to_db
#
#
# keywords = r"text_files/keywords.txt"
# stopwords = r"text_files/stopwords.txt"
# stopusers = r"text_files/stopusers.txt"
#
#
# insert_keywords_to_db(keywords)
# insert_stopusers_to_db(stopusers)
# insert_stopwords_to_db(stopwords)

from sql_inserts import insert_all_init

insert_all_init()