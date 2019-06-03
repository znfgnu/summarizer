# Summarizer

## Agents

- Chatbot
- Dispatcher
- Fetcher(s)
- Summarizer(s)
- Judge

## Message types
### 1. Chatbot -> dispatcher

Query generated after User's request to chatbot.
 
Fields:
- uuid: system-wide identifier for given User's request

Content (text): User's chosen topic

### 2. Dispatcher -> Fetcher(s)

Dispatcher forwards whole query to Fetchers - chatbot doesn't know about their presence. Fields are the same as in 1.

### 3. Fetchers -> Dispatcher

Fetchers are sending back to dispatcher list of articles that match given query.

Fields:
- uuid

Content (list): articles' JSONs

### 4.1. Dispatcher -> Summarizers
Dispatcher merges all articles into one text blob (sorted by published time) and sends it to Summarizers.

Fields:
- uuid
- judge JID

Content (text): Merged articles into one blob.

### 4.2. Dispatcher -> Judge

Dispatcher needs to register action with given UUID, so Judge know that has work to do.
This message also contains merged summaries gathered from fetchers, so Judge can store this information to calculate the marks. 

Fields:
- uuid
- timeout: time in seconds how much time Judge needs to wait for summaries to arrive. After timeout he uses only summaries
that already arrived
- max_summaries: how many summaries are about to come - after getting all of them, he can do its job.

Content (text): Concatenated summaries.

### 5. Summarizers -> Judge

Fields:
- uuid

Content (text): Summary

### 6. Judge -> Chatbot

Fields:
- uuid

Content (text): The best summary based on calculations.