HW5
================
Willie Langenberg
2020-12-03

## Exercise 1: Lööf vs Löfven

### a)

We start by importing the data. The data is given in the format of a R
access point, so by using the function “load” we can then access the
tables. We then create a column “Person” in each of the two tables, and
assign the value for whom the data is regarding. After this we can
simply join the tables with “bind\_rows”. We then filter for unique
tweets based on the “status\_id” and “Person”.

``` r
#Loading the data
load("../HW_data/LoofLofvenTweets.Rdata")

#Creating column of what person the data is regarding
Lofven <- Lofven %>% mutate(Person = "Löfven")
Loof <- Loof %>% mutate(Person = "Lööf")

#Joining the two tables, and deleting duplicate observations (identical tweets)
tweets <- Loof %>% 
  bind_rows(Lofven) %>%
  distinct(status_id, Person, .keep_all = TRUE)

tweets2 <- bind_rows(Lofven,Loof) %>%
  distinct(status_id, .keep_all = TRUE)

tweets3 <- Loof %>% 
  bind_rows(Lofven) %>%
  distinct(status_id, .keep_all = TRUE)
```

### b)

If we want to illustrate the intensity of the word “statsminister” for
each person we first have to do some calculations. We start by grouping
by person, then filter for texts including the word “statsminister”.
Note that we want to filter for both “statsminister” and “Statsminister”
because the pattern is case sensitive. After this we simply count the
number of appearances for each day, grouped by person. I chose to plot
this using a lineplot, because it is easy to spot trends over time and
easy to compare between the two persons.

``` r
#Counting and plotting the intensity of the word "Statsminister" in the tweets for Lööf and Löfven
tweets %>%
  group_by(Person) %>%
  filter(str_detect(text, pattern = or("Statsminister", "statsminister"))) %>%
  mutate(Date = as.Date(created_at)) %>%
  count(Date, name = "Count") %>%
  ggplot(aes(x = Date, y = Count, color = Person)) + geom_line(size=1) +
  labs(title="Lineplot", y = "Number of tweets", subtitle ="Daily intensity of tweets containing the word statsminster", caption = "Source: Twitter API (rtweet)")
```

![](HW5_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

### c)

In this assignment we are supposed to calculate and plot the average
sentiment of words for the two persons. I am not sure about what the
average sentiment really is but I think I know how to do the data
operations and calculation. We start by reading the data from the given
source. We create a new column “Date” in the “tweets” dataframe, which
is the date the tweet is created (without time-format). To get all words
for each day we use the given function “separate\_rows” on the “text”
column. To get each of these words’ sentiment value we have to join the
dataframes “tweets” and “sentiment\_df”. We do this with “inner\_join”.
Then we simply group by Person and Date and calculate the mean strength
of each word. I chose to plot the results with a lineplot once again.
From the plot we can say that Annie Lööf seems to have a slightly higher
average sentiment of words almost every day.

``` r
#Reading the data from the given data source. 
sentiment_df <- read_csv("https://svn.spraakdata.gu.se/sb-arkiv/pub/lmf/sentimentlex/sentimentlex.csv", col_names = TRUE, col=cols())

#Cleaning and merging the data before calculating the average sentiment of words, and then simply plotting the results
tweets %>%
  mutate(Date = as.Date(created_at)) %>%
  separate_rows(text) %>%
  select(Person, text, Date) %>%
  inner_join(sentiment_df, by=c("text" = "word")) %>%
  group_by(Person, Date) %>%
  summarize(AverageStrength = mean(strength), .groups = 'drop') %>%
  ggplot(aes(x = Date, y = AverageStrength, color = Person)) + geom_line(size = 1) +
  labs(title = "Lineplot", subtitle = "Daily average sentiment of words in tweets", y="Average Sentiment")
```

![](HW5_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

## Exercise 2: Nobel API

### a), b)

By looking into the documentation of The Nobel Price API we know how to
fetch the information trough the API. We want the Nobel prizes in
Literature in JSON format. The code is straightforward.

``` r
#Fetching the data with the Nobel Prize API
url <- "http://api.nobelprize.org/v1/prize.json?category=literature"
api_response <- GET(url)
nobel_df <- fromJSON(url)

#Reading in list of stop words
stop_words_url <- "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt"
stopwords <- read_table(stop_words_url, col_names = "word", col=cols())
```

Regarding the wordcloud, I couldn’t get wordcloud or wordcloud2 to work
when knitting to github\_document. I therefore chose to use the ggplot
method, with ggwordcloud library. To be able to fit all words so they
are readable, I had to remove some words with “rm\_outside = TRUE”.

``` r
#Binding the rows for the list "laureates", then anti_joining with the given stopwords dataframe. Then we count the number of repitions a word, and then we use wordcloud to plot the results. 
nobel_df[[1]]$laureates %>%
  bind_rows() %>%
  select(word = motivation) %>%
  separate_rows(word) %>%
  anti_join(stopwords, by="word") %>%
  filter(word != "", word != "I") %>% #Note that I manually deleted one more stopword (I), and the empy string ("").
  count(word, name="freq") %>%
  arrange(desc(freq)) %>%
  ggplot(aes(label = word, size = as.numeric(freq))) +
  geom_text_wordcloud_area(rm_outside = TRUE) +
  scale_size_area(max_size = 18) +
  theme_minimal()
```

    ## Some words could not fit on page. They have been removed.

![](HW5_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->
