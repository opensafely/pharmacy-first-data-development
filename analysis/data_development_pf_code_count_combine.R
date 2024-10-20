library(magrittr)
library(here)
library(readr)
library(dplyr)

# Load data
pf_codes_count_pathways <- read_csv(here("output", "data_development", "pf_codes_count_pathways.csv"))
pf_codes_count_events <- read_csv(here("output", "data_development", "pf_codes_count_events.csv"))
pf_codes_count_distinct <- read_csv(here("output", "data_development", "pf_codes_count_distinct.csv"))

df_tmp <- bind_rows(pf_codes_count_distinct, pf_codes_count_events, pf_codes_count_pathways)

# Write summary file
readr::write_csv(
  df_tmp,
  here::here("output", "data_development", "pf_codes_count_summary.csv")
)
