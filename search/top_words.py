from string import punctuation

def clean_data(text):
    """
    Parses an English text into a list of words. Ignores case and punctuation.

    Args:
        text (str): A string of text to parse.

    Returns:
        A list of words.
    """
    result = []
    original_words = text.split()
    for word in original_words:
        cleaned_word = word.strip(punctuation)
        if cleaned_word:
            result.append(cleaned_word)
    return result


def top_words(words):
    """
    Counts the frequency of words in <text>.

    Args:
        words (list): A list of words.

    Returns:
        A sorted list [(word1, freq1), (word2, freq2), ...] with frequencies in descending order.
    """
    result = {}
    for word in words:
        result.setdefault(word, 0)
        result[word] += 1

    # Sorted in descending order of frequency. If two words have the same frequency, sort in ascending ASCII order.
    return [(word, freq) for word, freq in sorted(list(result.items()), key=lambda x: (-x[1], x[0]))]


def tests():
    test_txt = "Subject: naturally irresistible your corporate identity  lt is really hard to recollect a company : the  market is full of suqgestions and the information isoverwhelminq ; but a good  catchy logo , stylish statlonery and outstanding website  will make the task much easier .  we do not promise that havinq ordered a iogo your  company will automaticaily become a world ieader : it isguite ciear that  without good products , effective business organization and practicable aim it  will be hotat nowadays market ; but we do promise that your marketing efforts  will become much more effective . here is the list of clear  benefits : creativeness : hand - made , original logos , specially done  to reflect your distinctive company image . convenience : logo and stationery  are provided in all formats ; easy - to - use content management system letsyou  change your website content and even its structure . promptness : you  will see logo drafts within three business days . affordability : your  marketing break - through shouldn ' t make gaps in your budget . 100 % satisfaction  guaranteed : we provide unlimited amount of changes with no extra fees for you to  be surethat you will love the result of this collaboration . have a look at our  portfolio _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ not interested . . . _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
    assert top_words(clean_data(test_txt)) == [('your', 7), ('will', 6), ('a', 5), ('and', 5), ('the', 5), ('of', 4), ('to', 4), ('company', 3), ('is', 3), ('logo', 3), ('that', 3), ('we', 3), ('you', 3), ('be', 2), ('become', 2), ('business', 2), ('but', 2), ('content', 2), ('do', 2), ('effective', 2), ('good', 2), ('in', 2), ('it', 2), ('make', 2), ('market', 2), ('marketing', 2), ('much', 2), ('not', 2), ('promise', 2), ('website', 2), ('100', 1), ('Subject', 1), ('affordability', 1), ('aim', 1), ('all', 1), ('amount', 1), ('are', 1), ('at', 1), ('automaticaily', 1), ('benefits', 1), ('break', 1), ('budget', 1), ('catchy', 1), ('change', 1), ('changes', 1), ('ciear', 1), ('clear', 1), ('collaboration', 1), ('convenience', 1), ('corporate', 1), ('creativeness', 1), ('days', 1), ('distinctive', 1), ('done', 1), ('drafts', 1), ('easier', 1), ('easy', 1), ('efforts', 1), ('even', 1), ('extra', 1), ('fees', 1), ('for', 1), ('formats', 1), ('full', 1), ('gaps', 1), ('guaranteed', 1), ('hand', 1), ('hard', 1), ('have', 1), ('havinq', 1), ('here', 1), ('hotat', 1), ('identity', 1), ('ieader', 1), ('image', 1), ('information', 1), ('interested', 1), ('iogo', 1), ('irresistible', 1), ('isguite', 1), ('isoverwhelminq', 1), ('its', 1), ('letsyou', 1), ('list', 1), ('logos', 1), ('look', 1), ('love', 1), ('lt', 1), ('made', 1), ('management', 1), ('more', 1), ('naturally', 1), ('no', 1), ('nowadays', 1), ('ordered', 1), ('organization', 1), ('original', 1), ('our', 1), ('outstanding', 1), ('portfolio', 1), ('practicable', 1), ('products', 1), ('promptness', 1), ('provide', 1), ('provided', 1), ('really', 1), ('recollect', 1), ('reflect', 1), ('result', 1), ('satisfaction', 1), ('see', 1), ('shouldn', 1), ('specially', 1), ('stationery', 1), ('statlonery', 1), ('structure', 1), ('stylish', 1), ('suqgestions', 1), ('surethat', 1), ('system', 1), ('t', 1), ('task', 1), ('this', 1), ('three', 1), ('through', 1), ('unlimited', 1), ('use', 1), ('with', 1), ('within', 1), ('without', 1), ('world', 1)]

if __name__ == '__main__':
    tests()
