library(tidyverse)
library(randomForest)
library(MASS)
library(gbm)

red_wine_df <- read.csv2("../Data/winequality-red.csv")
red_wine_df['wine_type'] = 1
white_wine_df <- read.csv2("../Data/winequality-white.csv")
white_wine_df['wine_type'] = 0

combined_df <- rbind(red_wine_df, white_wine_df)
combined_df_num <- as.data.frame(apply(combined_df, 2, FUN = as.numeric))
combined_df_num$quality <- ifelse(combined_df_num$quality < 5, 1, ifelse(combined_df_num$quality < 6, 2, ifelse(combined_df_num$quality > 6, 4, 3)))
combined_df_num$quality <- as.factor(combined_df_num$quality) 

#Shuffling the data
set.seed(9907)
shuffled_df <- combined_df_num[sample(nrow(combined_df_num)), ]

#Splitting the data
smp_size <- floor(0.80 * nrow(shuffled_df))
set.seed(9907)
train_ind <- sample(seq_len(nrow(shuffled_df)), size = smp_size)
training_df <- shuffled_df[train_ind, ]
testing_df <- shuffled_df[-train_ind, ]

model_lm <- glm(quality ~ fixed.acidity + volatile.acidity + citric.acid, data=as.data.frame(training_df), family = binomial)
preds_lm <- predict(model_lm, testing_df)
sum(as.integer(round(preds_lm, 0)) == testing_df$quality)/length(testing_df$quality)

model_rf <- randomForest(quality ~ ., data = as.data.frame(training_df))
preds_rf <- predict(model_rf, testing_df)
sum(as.integer(preds_rf == testing_df$quality)/length(testing_df$quality))

model_lda <- lda(quality ~ ., data = as.data.frame(training_df))
preds_lda <- predict(model_lda, testing_df)
sum(as.integer(preds_lda$class == testing_df$quality)/length(testing_df$quality))

model_gbm <- gbm(quality ~ ., data=as.data.frame(training_df), n.trees = 1500, interaction.depth = 5, n.minobsinnode = 0, shrinkage = 0.01)
preds_gbm <- predict(model_gbm, testing_df)
sum(as.integer(round(preds_gbm,0) == testing_df$quality)/length(testing_df$quality))

#Accuracy...


##########################################################
## O L D
#############################
# Splitting data into train/test set
# smp_size <- floor(0.80 * nrow(shuffled_df))
# train_ind <- sample(seq_len(nrow(shuffled_df)), size = smp_size)
# training_df <- shuffled_df[train_ind, ]
# testing_df <- shuffled_df[-train_ind, ]
# 
# set.seed(9907)
# model_rf <- randomForest(quality ~ ., data = as.data.frame(training_df))
# preds_rf <- predict(model_rf, testing_df)
# sum(as.integer(preds_rf == testing_df$quality)/length(testing_df$quality))
#############################
##
##########################################################
