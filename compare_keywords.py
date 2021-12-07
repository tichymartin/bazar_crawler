from data_file import stopusers_set, stopwords_set, keywords_set


def compare_keywords_one_link(single_data):
    user = set()
    user.add(single_data['user'])

    if stopusers_set.intersection(user):
        return

    elif stopwords_set.intersection(single_data["words_set"]):
        return

    elif keywords_set.intersection(single_data["words_set"]):
        single_data["keywords"] = set.intersection(keywords_set, single_data["words_set"])

        return single_data

    else:
        return


def compare_keywords(metadata):
    links_to_send_by_email = []

    for single_data in metadata:
        user = set()
        user.add(single_data['user'])

        if stopusers_set.intersection(user):
            # links_stopped_by_stop_users.append(metadata)
            continue

        elif stopwords_set.intersection(single_data["words_set"]):
            single_data["stopwords"] = set.intersection(stopwords_set, single_data["words_set"])
            # links_stopped_by_stopwords.append(metadata)
            continue

        elif keywords_set.intersection(single_data["words_set"]):
            single_data["keywords"] = set.intersection(keywords_set, single_data["words_set"])
            links_to_send_by_email.append(single_data)

        else:
            continue

    return links_to_send_by_email
