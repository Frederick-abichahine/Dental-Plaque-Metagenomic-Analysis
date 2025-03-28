# install.packages("ggplot2")     # For general plotting
# install.packages("dplyr")       # For data manipulation
# install.packages("readr")       # For reading CSV/TSV files
# install.packages("plotly")      # For interactive plots

# Load the libraries
library(ggplot2)
library(dplyr)
library(readr)
library(plotly)

checkm_data <- read_tsv("checkm_output.tsv")