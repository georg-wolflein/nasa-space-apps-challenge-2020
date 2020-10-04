library(word2vec)
library(dplyr)
library(textstem)

embedding<-NULL

word_embedding_featurization <- function(vecwords,j)
{
  temp <- rep(0,15)
  
  em <- embedding[intersect(unlist(vecwords),rownames(embedding)),]
  
  pass <- tryCatch({
  for(i in 1:15)
  {
    temp[i] = mean(unlist(em[,i]))
  }
  },error=function(condition){
    print(j)
    print(i)
    print(em)
    print(condition)})
  return(temp)
  
}

setwd("D:\\nasaapps")

raw.data <- read.csv("cleandataaboutdatasets.csv")

raw.data <- read.csv("..\\data.csv")

raw.data$x3 <- gsub(raw.data$x3,"[[:punct:]]","")
raw.data$x3 <- gsub(raw.data$x3,"[[:digits:]]","")
raw.data$x3 <- gsub(raw.data$x3,"[ ]+"," ")

raw.data$y <- gsub(raw.data$y,"[[:punct:]]","")
raw.data$y <- gsub(raw.data$y,"[[:digits:]]","")
raw.data$y <- gsub(raw.data$y,"[ ]+"," ")


raw.data$x3 <- lemmatize_strings(raw.data$x3)

raw.data$y <- lemmatize_strings(raw.data$y)

model <- word2vec(x = raw.data$x3, type="cbow", dim = 15, iter = 17)

embedding <- as.matrix(model)

split.data <- strsplit(raw.data$x3, " ")

new.data <- matrix(nrow=length(split.data),ncol=15,row.names=raw.data$X.1)

for(i in 1:length(split.data))
{
  new.data[i,] <- word_embedding_featurization(split.data[i],i)
  
  if(i %% 100 == 0) {print(i)}
}

write.csv(final.data, "featurized_data.csv")
