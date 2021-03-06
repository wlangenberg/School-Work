Case Study 1
================
Willie Langenberg
2021-02-28

## Exercise 1

We are given data generated by an AR model. We are then supposed to find
the number of lags used in the model, and it’s parameters. An important
note is that the lags is not above 5. This is essentially *order
determination*, so to find the number of lags one must calculate the AIC
for models with 1, 2, 3, 4 and 5 number of lags, and choose the one with
lowest AIC.

``` r
# Read the data
AR_df <- scan("AR.txt")

# Fit the data to an AR model with max 5 lags.
model <- ar(AR_df, AIC=TRUE, method="mle", order.max = 5)

# The function "ar" automatically fits the best model according to it's AIC. 
# We now want to see what amount of lags it used in the model.
model_ord <- model$order

# Parameters of the model
coeff <- model$ar
```

The best amount of lags to use according to AIC is then 3. The
parameters in the fitted AR(3) model are -0.1971113, 0.2953276,
0.0130519.

## Exercise 2

Given the data for U.S. quarterly real gross domestic product from 1947
to 2010, we are now going to test the null hypothesis

![equation](https://latex.codecogs.com/gif.latex?H_0%20%3A%20%5Crho_1%20%3D%20%5Crho_2%20%3D%20%5Cdotsc%20%3D%20%5Crho_%7B12%7D%20%3D%200)

against the alternative hypothesis

![equation](https://latex.codecogs.com/gif.latex?H_1%20%3A%20%5Crho_i%20%5Cneq%200%20%5Ctextrm%7B%20for%20some%20%7D%20i%20%5Cin%20%5C%7B%201%2C%5Cdotsc%2C12%20%5C%7D.)

We do this by using the Ljung-Box test. The test statistic is given by

![equation](https://latex.codecogs.com/gif.latex?Q%20%3D%20n%28n+2%29%5Csum_%7Bk%3D1%7D%5Eh%20%5Cfrac%7B%5Chat%7B%5Crho%7D_k%5E2%7D%7Bn-k%7D%2C)

where \(n\) is the number of observations, \(\hat{\rho}\) is the
autocorrelation at lag \(k\), and \(h\) is the number of lags being
tested. Under the null hypotheis, \(Q\) asymptotically follows a
\(\chi^2(h)\) distribution.

    ## 
    ##  Box-Ljung test
    ## 
    ## data:  growth_rate
    ## X-squared = 62.848, df = 12, p-value = 6.796e-09

With our data the \(Q\) statistic is \(62.848\). The p-value of the test
is very small (\<0.0001%), so we can safely reject the null hypothesis.
This suggests that the quarterly growth rate of the GDP is serially
correlated.

    ## [1] 3

Now we will build a simple AR model for the data. We choose the amount
of lags corresponding to the lowest AIC value. For our data, 3-lags gave
the lowest AIC. The estimates for this model is given by:

|           |             |
| :-------- | ----------: |
| ar1       |   0.3460663 |
| ar2       |   0.1298653 |
| ar3       | \-0.1224421 |
| intercept |   0.0079039 |

Before choosing this model we want to perform some model checking to see
if the model is adequate. If the model is adequate the residuals should
behave like white noise, which we can test by the Ljung-Box statistics.
The statistic is given by \(Q(m)\) as before, which follows a
chi-squared distribution with (m-g) degrees of freedom. The value of the
statistic is \(Q(12) =\) 12.964567 which follows a \(\chi^2(9)\)
distribution. The p-value is then 0.1642161. The p-value exceeds any
critical level and we can therefore reject the null hypothesis,
suggesting we have no serial correlation for the residuals. Further, we
can also test if the estimates are significantly different from zero. We
calculate the p-values to

|           | p-values         |
| :-------- | :--------------- |
| ar1       | 0.00000002414078 |
| ar2       | 0.04647485076783 |
| ar3       | 0.04871441192496 |
| intercept | 0.00000000000000 |

All estimates are shown to be significantly different from zero on the
\(5\%\) level. Hence, the model is now considered to be adequate.

### 

## Exercise 3

### Exercise 3.1

We have access to a dataset containing wages and other data for 474
employess of US bank. We consider a regression model given by:

![equation](https://latex.codecogs.com/gif.latex?Y_j%20%3D%20%5Cbeta_1%20+%20%5Cbeta_2E_j%20+%20%5Cbeta_3B_j%20+%20%5Cepsilon_j%2C%20j%20%3D1%2C%5Cdotsc%2Cn%2C)

where Y corresponds to the logarithm of the employees current salary, E
corresponds to EDUC, the number of finished education years and B
corresponds to the logarithm of the salary each employee started with at
the bank. We estimate the parameters of this model by solving the
equation

![equation](https://latex.codecogs.com/gif.latex?%5Chat%7B%5Cbeta%7D%20%3D%20%28X%5ETX%29%5E%7B-1%7DX%5ETy.)

Here we consider X to be the design matrix with every row corresponding
to a employee, the first column contains 1’s, the second contains the
number of education years for every employee and so on. Further, we
calculate the variance of the estimated \(\beta\)-parameters as

![equation](https://latex.codecogs.com/gif.latex?%5Chat%7BV%7D%28%5Chat%7B%5Cbeta%7D%29%20%3D%20s%5E2%28X%5ETX%29%5E%7B-1%7D%2C)

where \(s^2\) corresponds to the estimated sample variance given by

![equation](https://latex.codecogs.com/gif.latex?s%5E2%20%3D%20%5Cfrac%7Be%5ETe%7D%7Bn-k%7D%2C)

where \(e^te\) corresponds to the sum of the squared residuals and \(k\)
is the number of estimated parameters, 3.

This gives us the estimated parameters and standard deviations:

| parameter |  estimate |       std |
| :-------- | --------: | --------: |
| b\_1      | 1.6469157 | 0.2745981 |
| b\_2      | 0.0231223 | 0.0038936 |
| b\_3      | 0.8685045 | 0.0318346 |

We continue by now calculating the coefficient of determination
R<sup>2</sup> by

![equation](https://latex.codecogs.com/gif.latex?R%5E2%20%3D%201-%20%5Cfrac%7BRSS%7D%7BTSS%7D%2C)

which is calculated to \(R^2=\) 0.8005793, and the adjusted
R<sup>2</sup> is calculated as

![equation](https://latex.codecogs.com/gif.latex?%5Cbar%7BR%7D%5E2%3D%201%20-%20%5Cfrac%7BRSS/%28n-k%29%7D%7BTSS/%28n-1%29%7D%2C)

which is calcualted to \(\bar{R}^2=\) 0.7997325. We have a high
R<sup>2</sup> meaning the model fit to the data relatively good. Notice
that the adjusted R<sup>2</sup> is slightly lower, because it punishes
the model for additional variables, which means it can never be larger
than the regular R<sup>2</sup>.

We can control our calculations by using the R Summary function giving

    ## 
    ## Call:
    ## lm(formula = LOGSAL ~ EDUC + LOGSALBEGIN, data = bwa_df)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.45035 -0.11750 -0.01215  0.11453  0.90229 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept) 1.646916   0.274598   5.998 3.99e-09 ***
    ## EDUC        0.023122   0.003894   5.938 5.59e-09 ***
    ## LOGSALBEGIN 0.868505   0.031835  27.282  < 2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1778 on 471 degrees of freedom
    ## Multiple R-squared:  0.8006, Adjusted R-squared:  0.7997 
    ## F-statistic: 945.4 on 2 and 471 DF,  p-value: < 2.2e-16

Now we want to test for heteroskedasticity. We do this with White’s
test, having the null hypothesis of homoscedasticity. The method of this
test is to regress the residuals on the explanatory variables and their
squares and cross products. We start by fitting the model

![equation](https://latex.codecogs.com/gif.latex?%5Cepsilon_j%5E2%20%3D%20%5Clambda_1%20+%20%5Clambda_2X_%7B2j%7D%20+%20%5Clambda_3X_%7B3j%7D%20+%20%5Clambda_4X_%7B2j%7D%5E2%20+%20%5Clambda_5X_%7B3j%7D%5E2%20+%20%5Clambda_6X_%7B2j%7DX_%7B3j%7D%20+%20u_j%2C)

whereas on the null hypothesis, \(nR^2\) is asymptotically distributed
as \(\chi^2(5)\). We calculate the \(nR^2\) to 10.5483396, with the
corresponding p-value 0.0611081. The null hypothesis is barely not
rejected at the \(5\%\) level. We reject the null hypothesis which means
that we have heterskedasticity in the model.

To test for autocorrelation we use the Durbin-Watson’s test. This test
results in

    ## 
    ##  Durbin-Watson test
    ## 
    ## data:  model_1
    ## DW = 1.8211, p-value = 0.02483
    ## alternative hypothesis: true autocorrelation is greater than 0

hence we reject the null hypothesis of no autocorrelation.

### Exercise 3.2

Now we are going to include gender and minority as additional
explanatory variables. We fit this new model to our data which gives us
the summary

    ## 
    ## Call:
    ## lm(formula = LOGSAL ~ EDUC + LOGSALBEGIN + GENDER + MINORITY, 
    ##     data = bwa_df)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -0.45572 -0.11508 -0.00516  0.10765  0.87060 
    ## 
    ## Coefficients:
    ##             Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  2.07965    0.31480   6.606 1.07e-10 ***
    ## EDUC         0.02327    0.00387   6.013 3.66e-09 ***
    ## LOGSALBEGIN  0.82180    0.03603  22.808  < 2e-16 ***
    ## GENDER       0.04816    0.01991   2.419   0.0160 *  
    ## MINORITY    -0.04237    0.02034  -2.083   0.0378 *  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.1766 on 469 degrees of freedom
    ## Multiple R-squared:  0.8041, Adjusted R-squared:  0.8024 
    ## F-statistic: 481.3 on 4 and 469 DF,  p-value: < 2.2e-16

Notice that when including these new explanatory variables in the model
the estimates also changes for the first two explanatory variables. This
most likely comes from correlation among the explanatory variables. An
intuitive way to think about is with an simple example. If we have data
corresponding to a straight line and we try to fit only one variable,
the intercept, we might first have a positive intercept. However, when
adding another variable, the x-coordinate of every observation, we might
get a negative intercept and a much better fit to data. This principle
applies when having more variables aswell.

We move on with testing the joint significance of GENDER and MINORITY.
We have fitted both a model with and without them so we can easily use
restricted/unrestricted regression method to test this. The unrestricted
model is the last model including gender and minority and the restricted
model is the first model without them. We test this using the
F-statistic

![equation](https://latex.codecogs.com/gif.latex?F%20%3D%20%5Cfrac%7B%28RSS_r-RSS_u%29/q%7D%7BRSS_u/%28n-k%29%7D%2C)

where \(RSS_r\) is the residual sum of squares of the restricted model,
\(q\) is the number of restrictions imposed and \(k\) is the number of
parameters estimated in the unrestricted model. The F-statistic in our
case is 4.2349461 which is F(2, 469)-distributed. The p-value is then
0.0150382, which means that we reject the null hypothesis of the
restricted model. This means that the additional variables added in the
new model is not significant.

Further we now want to test whether the coefficient for education is
different from zero. In both our models we can see from the summaries
that education was significantly different from zero with p-values lower
than \(0.1\%\). From this I conclude that education is very important
when it comes to salary, which is really no surprise.

We can also test the significance of the regression, meaning that the
null hypothesis is that all estimates of the explanatory variables is
zero. The “restricted” model would then be just the intercept, that
simply equals the mean of the response variable. This test is also
automatically calculated in the summaries. In all models we have
p-values less than \(0.01\%\).
