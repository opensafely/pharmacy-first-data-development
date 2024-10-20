library(magrittr)
library(here)
library(readr)
library(dplyr)

# Load data
df_tmp <- read_csv(here("output", "data_development", "pf_codes_data_development.csv.gz"))

print("Load data successfully")

# Restructure data into 'long' format
# Removing the leading "_" using `stringr::str_sub` isnt elegant but I dont know
# how to do this using regex.
df_tmp <- df_tmp %>%
dplyr::select(
  pre_all_count_pf_pathways,
  pre_pfid_count_pf_pathways,
  pre_pfdate_count_pf_pathways,
  post_all_count_pf_pathways,
  post_pfid_count_pf_pathways,
  post_pfdate_count_pf_pathways
) %>%
  tidyr::pivot_longer(
    cols = c(
      "pre_all_count_pf_pathways",
      "pre_pfid_count_pf_pathways",
      "pre_pfdate_count_pf_pathways",
      "post_all_count_pf_pathways",
      "post_pfid_count_pf_pathways",
      "post_pfdate_count_pf_pathways"
    ),
    names_to = c("time", "selected_events_and_summary_stat"),
    names_sep = "(?<=pre|post)"
  )

print(paste0("df_tmp: ", object.size(df_tmp), " bytes"))
print("Pivot data successfully")

df_tmp <- df_tmp %>%
  dplyr::mutate(selected_events_and_summary_stat = stringr::str_sub(selected_events_and_summary_stat, 2, -1)) %>%
  tidyr::separate(selected_events_and_summary_stat, into = c("selected_events", "summary_stat"), sep = "(?<=all|pfid|pfdate)") %>%
  dplyr::mutate(summary_stat = stringr::str_sub(summary_stat, 2, -1))

print(paste0("df_tmp: ", object.size(df_tmp), " bytes"))
print("Tidy data successfully")

# Calculate sum and apply statistical disclosure control
df_tmp <- df_tmp %>%
  dplyr::group_by(time, selected_events, summary_stat) %>%
  dplyr::mutate(count = sum(value, na.rm = TRUE)) %>%
  dplyr::ungroup() %>%
  dplyr::arrange(summary_stat, selected_events, dplyr::desc(time)) %>%
  dplyr::filter(count > 7) %>%
  dplyr::mutate(count = round(count, -1)) %>%
  dplyr::select(time, selected_events, summary_stat, count) %>%
  dplyr::distinct()

print(paste0("df_tmp: ", object.size(df_tmp), " bytes"))
print("Summarise data successfully")

# Write summary file
readr::write_csv(
  df_tmp,
  here::here("output", "data_development", "pf_codes_count_pathways.csv")
)
