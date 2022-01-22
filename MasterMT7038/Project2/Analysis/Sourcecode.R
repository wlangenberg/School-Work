# Loading packages used for later analysis
library(tidyverse)
library(gbm)

# Reading in the data.
setwd("~/Documents/Statistical Learning/Project 2/")
url <- "Data/data.txt"
df <- read.table(url)


# Task 1 - a) Fitting a gradient boosting tree:
model_1 <- gbm(V58 ~ ., data=df, distribution = "bernoulli", n.trees = 1500, interaction.depth = 1, n.minobsinnode = 0, shrinkage = 0.01)

# Task 2 - b) Construct gradient boosting trees with different number of nodes. 
gradient_boosted_trees_node <- function(data_df, nodes, trees=1500, folds=0) {
  boosted_model <- gbm(V58 ~ ., data=data_df, distribution = "bernoulli", n.trees = trees, interaction.depth = nodes, n.minobsinnode = 10, shrinkage = 0.01, cv.folds = folds)
  return(boosted_model)
} 

### Stump
stump_model <- gradient_boosted_trees_node(df, 1)
### 5
node_5_model <- gradient_boosted_trees_node(df, 5)
### 10
node_10_model <- gradient_boosted_trees_node(df, 10)
### 20
node_20_model <- gradient_boosted_trees_node(df, 20)
### etc...


# Task - c) Cross-validation
misclassification_error <- function(x, y) {
  return (sum(x!=y$V58)/length(x))
}

cv_error_est <- function(x) {
  return (c(mean(x),sd(x)/sqrt(length(x))))
}

crossvalidation_errors <- function(data=df, M=100, step=50) {
  # Starting by shuffle the data
  df_shuffled <- df[sample(nrow(df)),]
  # Creating 10 folds, to use on all models
  cv_folds <- cut(seq(1,nrow(df_shuffled)), breaks=10, labels=FALSE)
  #Variable to store results for each fold
  error_rates <- NULL
  # For each fold, train on 9 folds and use the remaining as test set.
  for(i in 1:10){
    print(c('Fold:', i))
    # Splitting data accoring to cross validation folds
    kfold_index <- which(cv_folds == i,arr.ind=TRUE)
    testData <- df_shuffled[kfold_index, ]
    trainData <- df_shuffled[-kfold_index, ]
    # Train a gradient boosted model with only a stump, interaction depth = 1, trees = m, and with 10-fold cv.
    model <- gradient_boosted_trees_node(trainData, nodes = 1, trees = M, folds=0)
    #predict using different amount of trees
    preds <- predict.gbm(model, testData, seq(step, M, step))
    # Convert predictions to classes (0,1)
    preds_class <- apply(preds>0, FUN = as.integer, 2)
    # misclassification on test data for each fold
    misclass_error_rate <- apply(preds_class, 2, FUN = misclassification_error, y = testData)
    error_rates <- rbind(error_rates, misclass_error_rate)
  }
  # Calculate mean and standard error for the cv estimated errors.
  output <- apply(error_rates, 2, FUN = cv_error_est)
  output <- as_tibble(cbind(c(output[1,]), c(output[2,]))) %>% 
    mutate("x" = seq(step, M, step)) %>%
    rename(mean = V1, se = V2)
  
  return(output)
}

cv_error_est <- crossvalidation_errors(df, 5000, 100)

cv_error_est %>% ggplot(aes(x=x, y=mean)) + 
  theme_minimal() + 
  geom_line(color="darkblue") + 
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), color="orange") + 
  geom_point(color="darkblue") + 
  xlab("Number of trees") + 
  ylab("CV Error")

# Lowest CV (4600 number of trees)
lowest_cv <- cv_error_est[which.min(cv_error_est$mean), ]
lowest_cv_se <- lowest_cv$mean + lowest_cv$se

# CV within 1 standard error (2000 trees)
cv_error_est[cv_error_est$mean<lowest_cv_se,][1,]
