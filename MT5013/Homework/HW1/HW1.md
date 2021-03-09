HW1
================
Willie Langenberg
2020-11-02

## Past experiences

In past courses in mathematical statistics, we have always used R for
writing the reports. With that said, I am somewhat familiar with the
syntax in R, R Studio and R markdown. I have also used some “ggplot2”,
to plot nice looking graphics. However I have never used Git, Github or
dplyr before.

## Data Example

Today the temperature felt unusually warm (14°C) for a november day in
Stockholm. I figured I wanted to see some historical data for the
temperature at this time of the year (2nd day of November). I simply
used Google to search for “temperature dataset in sweden” and found
“<https://bolin.su.se/data/stockholm-thematic/air_temperature.php>”.
It is a centre for climate research with open access datasets. On the
website I chose to download data for the homogenized daily mean
temperatures. The data came in the format of a textfile with
tabseperated columns. To read it into R I used the function
“read.table”, which creates a dataframe to store the data in. The
plot in *Figure.1* below shows the historical mean temperature of every
2th of November day, from 1756 to 2005.

``` r
library(ggplot2)
df <-  read.table("daily_temp.txt")
df <- df[c(1, 2, 3, 6)]
names(df) <- c("Year", "Month", "Day", "Temperature")
new_df <- subset(df, df[2]==11 & df[3]==2)

ggplot(new_df, aes(Year, Temperature)) + geom_point()
```

![Plot that shows the mean temperature of each 2nd of November day, from
1756 to 2005.](HW1_files/figure-gfm/unnamed-chunk-1-1.png)

*Figure 1:* Plot that shows the mean temperature of each 2nd of November
day, from 1756 to 2005.

``` r
sessionInfo()
```

    ## R version 4.0.3 (2020-10-10)
    ## Platform: x86_64-pc-linux-gnu (64-bit)
    ## Running under: Ubuntu 16.04.7 LTS
    ## 
    ## Matrix products: default
    ## BLAS:   /usr/lib/atlas-base/atlas/libblas.so.3.0
    ## LAPACK: /usr/lib/atlas-base/atlas/liblapack.so.3.0
    ## 
    ## locale:
    ##  [1] LC_CTYPE=C.UTF-8       LC_NUMERIC=C           LC_TIME=C.UTF-8       
    ##  [4] LC_COLLATE=C.UTF-8     LC_MONETARY=C.UTF-8    LC_MESSAGES=C.UTF-8   
    ##  [7] LC_PAPER=C.UTF-8       LC_NAME=C              LC_ADDRESS=C          
    ## [10] LC_TELEPHONE=C         LC_MEASUREMENT=C.UTF-8 LC_IDENTIFICATION=C   
    ## 
    ## attached base packages:
    ## [1] stats     graphics  grDevices utils     datasets  methods   base     
    ## 
    ## other attached packages:
    ## [1] ggplot2_3.3.2
    ## 
    ## loaded via a namespace (and not attached):
    ##  [1] knitr_1.30       magrittr_1.5     tidyselect_1.1.0 munsell_0.5.0   
    ##  [5] colorspace_1.4-1 R6_2.4.1         rlang_0.4.8      highr_0.8       
    ##  [9] stringr_1.4.0    dplyr_1.0.2      tools_4.0.3      grid_4.0.3      
    ## [13] gtable_0.3.0     xfun_0.18        withr_2.3.0      htmltools_0.5.0 
    ## [17] ellipsis_0.3.1   yaml_2.2.1       digest_0.6.25    tibble_3.0.4    
    ## [21] lifecycle_0.2.0  crayon_1.3.4     farver_2.0.3     purrr_0.3.4     
    ## [25] vctrs_0.3.4      glue_1.4.2       evaluate_0.14    rmarkdown_2.4   
    ## [29] labeling_0.3     stringi_1.5.3    compiler_4.0.3   pillar_1.4.6    
    ## [33] generics_0.0.2   scales_1.1.1     pkgconfig_2.0.3
