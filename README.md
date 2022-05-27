Josh Coward and Sam Jackson CS 437

Project 1

Search Engine Report

**Implementation of Text Processing :**

For the implementation of this project we used a lot of code from the previous homeworks as a starting point. The tokenizer we used was once again the work\_tokenize from nltk and again we opted for lemmatization rather than stemming in our preprocessing using nltk’s WordNetLemmatizer. This was due to the fact that stemming resulted in a lack of meaning which makes it harder to return relevant results. We also used ntlks english stopword list in which we had appended punctuation to it to help remove the /r and /n present in the content of each document.

**Statistics on Document Collection:**

The number of documents present: 1,286,264 Index size prior to preprocessing: 244,435,249 Index size after preprocessing: 2,651,233

**Implementation of Query Suggestions:**

To implement query suggestions, we imported the query log into a dataframe to make manipulating the data easier. In this case, it was simpler to use a dataframe but to make it more efficient a dictionary could be used. We wrote a method that takes the query as a parameter and outputs all queries that begin with the input (excluding an exact match, as suggesting the inputted query would be pointless). These results are sorted by frequency, so the queries that q’ are most often modified to are presented first, as intended by the 𝑆𝑐𝑜𝑟𝑒(𝐶𝑄, 𝑞′) equation.

**Implementation of Ranking:**

Like instructed, the way we went about coming up with our ranking system was by using the inverted\_index which in our case consisted of a dictionary where the key was equal to the specific word and the value was equal to a list of all the documents that the word could be found in. In our case we opted to account for the number of occurrences of each word in a particular document later outside the inverted\_index in the case if the word appeared in the query in order to achieve a faster and more efficient computation.

To rank results, first we would read in the users query. The query was then cleaned to fit the preprocessing that all the words in the inverted index had experienced. From there we created a list of documents that consisted of all the documents in common between the query terms. If there were less than 50 documents in total we would take whatever documents remained in the query term that resulted in the least amount of total documents that that word was found in. We did this because the word with less occurrences was seen as more rare and therefore a better use in finding accurate results rather than using the more common query term.

From there we performed the actual ranking portion given a list of potential candidate documents retrieved from the previous step and ranked them similarly to how we ranked documents in homework 4: by taking the number of occurrences of a word in a document and dividing that number by the total number of words in that document. That value was then multiplied by the total number of documents in which the word appeared and divided by the total number of documents in the collection. For any word that was unseen before and or not in the inverted index a smoothing value of 0.00001 was applied in order to avoid errors due to dividing by 0.

The documents were then added to a dictionary where the key was the Document ID number and the value was the probability of getting that document given the query in question. This dictionary was then sorted by descending order of value. Then a second dictionary was made and where the key was once again the document ID number and the value was a nested dictionary where the first key was the title of the document and the

corresponding value was the actual title of that document. The second and last key in the nested dictionary’s key was content and it’s value consisted of the result of the cosine similarity between the query and the content of the document where the result was a sentence that contained the most related sentence to the query.This value was then sent over flask to an html page to be displayed in the browser.

The purpose of using dictionaries in this project served multiple purposes. One being that it allowed a lookup time of O(1) which is about as fast as you can get. Also flask will only allow dictionaries and strings to be sent over to an ajax function in javascript so using a dictionary was a must.

**Implementation of snippet generation:**

To generate snippets of relevant documents, we found the two sentences with the highest cosine similarity score with the query in each document. Originally, we used a dataframe to store this information but we chose to switch to a dictionary for efficiency, as the previous method slowed the calculation of results. To calculate the cosine similarity, we used the sklearn library’s TfIdfVectorizor function to create a matrix of TF-IDF scores for each word in the query and each sentence in a document. We also used sklearn’s cosine\_similarity function to compare the relevancy of sentences, using the TF-IDF matrix as input, as it is an efficient implementation of the calculation that uses smoothing to avoid division by zero.

In some documents, there may be only one sentence that is of importance to the user based on the query. In these cases, we chose to only return one sentence instead of presenting one relevant sentence and one irrelevant sentence, as we felt that is more practical for a user.

**Discussion:**



|**Query:**||Fried Chicken||
| - | :- | - | :- |
|**Ranking**|**Document ID**|**Snippet**|**Ranking Score**|
|**1**|767511|<p>'sentence1': 'Tastee Fried Chicken Tastee Fried Chicken (also known as "TFC" or "De Tastee Fried Chicken Nigeria LTD") is a fast food fried chicken restaurant based in Victoria Island, Lagos, Nigeria.',</p><p>'sentence2': "In 2006, Tastee Fried Chicken launched a partnership with Oando, a petroleum company, that has begun locating Tastee Fried Chicken restaurants inside Oando's service stations."</p>|5.307e-09|
|**2**|1271085|<p>'sentence1': 'It started as a pizzeria; however, later its owners decided to finally go into the fried chicken market.',</p><p>'sentence2': ' '</p>|1.968e-09|
|**3**|549593|<p>'sentence1': 'The primary factor that distinguishes Maryland fried chicken from other Southern fried chicken is that rather than cooking the chicken in several inches of oil or shortening, the chicken is pan-fried in a heavy (traditionally cast-iron) skillet and covered tightly after the initial browning so that the chicken steams as well as fries.',</p><p>'sentence2': 'Other reported versions include: a fried chicken leg with ham and hush puppies (a batter made with flour, egg, oil, and milk or water, to which corn is added, then deep-fried); batter-fried chicken with hush-puppies and batter-fried bananas and pineapple rings; and bread-crumbed and fried chicken wings & drumsticks with sautéed</p>|1.366e-09|


|||bananas.'||
| :- | :- | - | :- |
|**4**|95089|<p>'sentence1': 'The restaurant serves fried chicken, catfish, chicken tenders, and side dishes.',</p><p>'sentence2': "Chicken Express was established in 1988 by Richard and Nancy Stuart's Stuart Group Inc."</p>|1.09e-09|
|**5**|924616|<p>'sentence1': 'In 1996, Golden Fried Chicken abbreviated to its present name, Golden Chick.',</p><p>'sentence2': 'The first restaurant was in 1967 in San Marcos, Texas, under the name Golden Fried Chicken.'</p>|7.084e-10|
We used the above query as just a basic test for the search engine, the intent was to see if we actually got results that had the bigram “fried chicken” in it just to see that it was working as intended. From the results it would appear that we had retrieved relevant documents.



|**Query:**||Fried Chicken recipe||
| - | :- | - | :- |
|**Ranking**|**Document ID**|**Snippet**|**Ranking Score**|
|**1**|549593|<p>'sentence1': 'The primary factor that distinguishes Maryland fried chicken from other Southern fried chicken is that rather than cooking the chicken in several inches of oil or shortening, the chicken is pan-fried in a heavy (traditionally cast-iron) skillet and covered tightly after the initial browning so that the chicken steams as well as fries.',</p><p>'sentence2': 'Other reported versions include: a fried chicken leg with ham and hush puppies (a batter made with flour, egg, oil, and milk or water, to which corn is added, then deep-fried); batter-fried chicken with hush-puppies and batter-fried bananas and pineapple</p>|2.202e-14|


|||rings; and bread-crumbed and fried chicken wings & drumsticks with sautéed bananas.'||
| :- | :- | :- | :- |
|**2**|552650|<p>'sentence1': 'Chicken balls  Chicken balls are a food consisting of small, spherical or nearly spherical pieces of chicken.',</p><p>'sentence2': 'The dish consists of small chunks of fried chicken breast meat covered in a crispy batter coating.'</p>|5.099e-15|
|**3**|820135|<p>'sentence1': 'It is famous for its skinless fried chicken products and for their signature fried chicken having 25% less fat than traditional fried chicken.',</p><p>'sentence2': "Pudgie's Famous Chicken was founded in 1981 in Bethpage, New York by George Sanders, who developed a secret batter recipe and skinning progress."</p>|3.759e-15|
|**4**|895406|<p>'sentence1': 'It was originally called Chicken and Spice and Virginia Fried Chicken.',</p><p>'sentence2': 'While the recipe was not published, the chicken was cooked in special pressure-cookers and the process involved soaking the chicken in salt water.'</p>|3.188e-15|
|**5**|356290|<p>'sentence1': 'Chicken Marengo  Chicken Marengo is a French dish consisting of a chicken sautéed in oil with garlic and tomato, garnished with fried eggs and crayfish.',</p><p>'sentence2': 'The dish is similar to chicken à la Provençale, but with the addition of egg and crayfish, which are traditional to Chicken Marengo but are now often omitted.'</p>|2.238e-15|
The intent behind the above query was to find relevant recipes for fried chicken. Looking at the results it looks like our search engine was on the right track as the top results contained steps in making fried chicken.

However, none of the results contained information on quantities and any real linear start to finish path for making fried chicken but just generally how it was made at a restaurant. This is probably just a dataset issue more than anything.



|**Query:**||Donald Trump||
| - | :- | - | :- |
|**Ranking**|**Document ID**|**Snippet**|**Ranking Score**|
|**1**|4521|<p>'sentence1': 'List of proclamations by Donald Trump  Listed below is the Presidential proclamations beginning with signed by United States President Donald Trump.',</p><p>'sentence2': '<onlyinclude>As of January 4, 2018, there have been 118 Presidential proclamations signed by President Trump.</onlyinclude>'}</p>|5.432e-09|
|**2**|8187|<p>'sentence1': "Nazakhtar Nikakhtar Nazakhtar Nikakhtar is an American lawyer and President Donald Trump's nominee for Assistant Secretary of Commerce (Industry and Analysis).",</p><p>'sentence2': ' '</p>|4.400e-09|
|**3**|1061583|<p>'sentence1': 'In the census of 1911 there were 32 registered family names Birthplace of Donald Trump',</p><p>'sentence2': ' '</p>|4.068e-09|
|**4**|911539|<p>'sentence1': 'In February 2017, the newspaper received international attention when it mistakenly published an image of Alec Baldwin portraying Donald Trump, the 45th President of the United States, instead of Donald Trump himself.',</p><p>'sentence2': ' '</p>|1.636e-09|
|**5**|1098747|'sentence1': 'Voted for Donald Trump and Mike Pence:  Voted for Mitt Romney and Paul Ryan:   Voted for John McCain|1.193e-09|


|||<p>and Sarah Palin:',</p><p>'sentence2': ' '</p>||
| :- | :- | - | :- |
The intent in the query above was to retrieve information on former president Donald Trump. The results were questionable in this case as certainly the top results contain instances of the “donald trump” in them, but the content of them was quite short so there was a lack of information.



|**Query:**||Barack Obama||
| - | :- | - | :- |
|**Ranking**|**Document ID**|**Snippet**|**Ranking Score**|
|**1**|148539|<p>'sentence1': 'Obama (disambiguation) Barack Obama (born 1961) is a former President of the United States.',</p><p>'sentence2': 'Obama may also refer to:'</p>|3.45e-09|
|**2**|379986|<p>'sentence1': 'David Axelrod (disambiguation)  David Axelrod (born 1955) is a senior advisor to former U.S. President Barack Obama.',</p><p>'sentence2': ' '</p>|8.547e-10|
|**3**|1062747|<p>'sentence1': 'She continued to serve in that position in the Administration of President Barack Obama until Mr. Obama named Cindy S. Moelis as her successor in April 2009.',</p><p>'sentence2': ' '</p>|5.118e-10|
|**4**|971177|<p>'sentence1': 'US President Barack Obama stayed there in his visit in April 2014.',</p><p>'sentence2': ' '</p>|4.075e-10|
|**5**|136115|<p>'sentence1': 'Senators have won: Barack Obama, Everett Dirksen, Al Franken, and Hillary Clinton.',</p><p>'sentence2': ' '</p>|1.963e-10|
Like the previous query, the intent in the query above was to retrieve information on the past president Barack Obama in hopes to find better results than were found for Donald Trump. Again the results were questionable but slightly better then the previous query as there was more specific information about Barack than Donald but still the overall content of each document was pretty small.



|**Query:**||Pizza||
| - | :- | - | :- |
|**Ranking**|**Document ID**|**Snippet**|**Ranking Score**|
|**1**|495692|<p>'sentence1': 'Pizza Connection  Pizza Connection may refer to:',</p><p>'sentence2': ' '</p>|0.000227|
|**2**|505841|<p>'sentence1': 'Pizza (disambiguation) Pizza is a popular Italian dish.',</p><p>'sentence2': 'Pizza may also refer to:'</p>|0.001609|
|**3**|855257|<p>'sentence1': '241 Pizza competes with other pizza chains such as Pizza Pizza, Pizza Hut, Little Caesars, and Pizza Nova.',</p><p>'sentence2': '241 Pizza was founded in Toronto in 1986.'</p>|0.000107|
|**4**|323685|<p>'sentence1': 'The stuffed crust pizza was popularized by Pizza Hut which debuted this style of pizza in 1995.',</p><p>'sentence2': 'Pizza Hut hired Donald Trump to advertise the pizza.'</p>|9.560e-05|
|**5**|1099551|<p>'sentence1': 'Other pizza companies also later included pan pizza.',</p><p>'sentence2': "In 1989, Domino's Pizza introduced its deep dish or pan pizza."</p>|8.744e-05|
Lastly as the unigram test we tested the query “pizza”  to see what information we could get on it. In this case given that we only searched for pizza without any sort of context I would say the results were very good as they consisted of either restaurant information that served pizza or an actual definition of pizza.

Overall based on the results from each of the individual queries I would say that the results were as good as one could expect using our ranking algorithm and the given dataset. For certain queries such as the ones that consisted of past president names the results were slightly underwhelming in that they didn’t possess as much information on the president as I would hope. The top results just happened to be a sentence long which just makes the ratio of the president's name high in the document being that there's only a handful of words in total in the first place. So it makes sense that we got those results. For the other queries like fried chicken/fried chicken recipes and pizza I was honestly impressed how good the results were. Most of them weren’t short in content length and actually contained information one might hope to retrieve given this dataset. As far as the project goes overall I would say in general it went rather smoothly. The biggest issue we ran into and will most certainly try to address for project 2 is dealing with and processing such a large dataset. There were multiple times when preprocessing functions had to be rewritten in order to achieve a realistic computation time relative to when the project was due. The decision to compute the number of occurrences of a word in a document during the time of searching rather than with the creation of the inverted index was made so that the inverted index wouldn't take days/weeks to compute. However this did lead to a slower searching time ultimately which we intend to address in the next project as well. To add to that, there was also the issue of running out of RAM due to needing to access the two datasets along with the inverted index on top of the frontend portion. Fortunately due to having access to a physical server this problem was easily fixed when attempting to run the entire project. However for testing we used subsets of the data in order to understand how the program was functioning as we developed it.



|**Query:**|fried chicken||
| - | - | :- |
|**Ranking**|**Candidate Suggestion**|**Score**|
|**1**|fried chicken recipes|0.42|
|**2**|fried chicken recipe|0.210|
|**3**|fried chicken cookers|0.105|
|**4**|fried chicken concession trailers|0.052|
|**5**|fried chicken wings|0.052|


|**Query:**|Fried chicken recipe||
| - | - | :- |
|**Ranking**|**Candidate Suggestion**|**Score**|
|**1**|Fried chicken recipes|1|
|**2**|none|0|
|**3**|none|0|
|**4**|none|0|
|**5**|none|0|


|**Query:**|Donald trump||
| - | - | :- |
|**Ranking**|**Candidate Suggestion**|**Score**|
|**1**|donald trump baby|0.101|
|**2**|donald trump’s baby|0.050|
|**3**|donald trump seminar|0.050|
|**4**|donald trump the apprentice|0.033|


|**5**|donald trump’s children|0.033|
| - | - | - |


|**Query:**|Barack Obama||
| - | - | :- |
|**Ranking**|**Candidate Suggestion**|**Score**|
|**1**|none|0|
|**2**|none|0|
|**3**|none|0|
|**4**|none|0|
|**5**|none|0|


|**Query:**|pizza||
| - | - | :- |
|**Ranking**|**Candidate Suggestion**|**Score**|
|**1**|pizza hut|1.659|
|**2**|pizza hut coupons|0.054|
|**3**|pizza dough|0.054|
|**4**|pizza pan|0.030|
|**5**|pizza delivery|0.030|
Results from Wikipedia:

**Query:** fried chicken![](Aspose.Words.ce52cff0-d5a5-4509-9ed9-8112e955e41d.001.png)



|**Ranking**|**Document Title**|
| - | - |
|**1**|Fried chicken|
|**2**|KFC|
|**3**|Chicken fried steak|
|**4**|Korean fried chicken|
|**5**|Popeyes|


|**Query:** fried chicken recipe|
| - |
|**Ranking**|**Document Title**|
|**1**|Fried chicken|
|**2**|KFC Original Recipe|
|**3**|KFC|
|**4**|Chicken fried steak|
|**5**|Crispy fried chicken|


|**Query:** Donald Trump|
| - |
|**Ranking**|**Document Title**|
|**1**|Donald Trump|
|**2**|Donald Trump Jr.|
|**3**|Presidency of Donald Trump|
|**4**|Family of Donald Trump|
|**5**|Donald Trump 2016 presidential campaign|


|**Query:** Barack Obama|
| - |
|**Ranking**|**Document Title**|
|**1**|Barack Obama|
|**2**|Barack Obama Sr.|
|**3**|Family of Barack Obama|
|**4**|Presidency of Barack Obama|
|**5**|Barack Obama citizenship conspiracy theories|


|**Query:** Pizza|
| - |
|**Ranking**|**Document Title**|
|**1**|Pizza|
|**2**|Pizza Hut|
|**3**|Pizza Pizza|
|**4**|&pizza|
|**5**|Hawaiian pizza|

