library(magrittr)
library(arrow)
# Load data
df_med_status <- arrow::read_feather(
  here::here("output", "data_development", "med_status_data_development.arrow")
)

print("Load data successfully")

selected_variables_list <- list(
  "pre_any" <- paste0("pre_any_", paste0("status", 0:28)),
  "pre_pfmed" <- paste0("pre_pfmed_", paste0("status", 0:28)),
  "pre_pfmedid" <- paste0("pre_pfmedid_", paste0("status", 0:28)),
  "pre_any_pfid" <- paste0("pre_any_pfid_", paste0("status", 0:28)),
  "pre_date_pfid" <- paste0("pre_date_pfid_", paste0("status", 0:28)),
  "post_any" <- paste0("post_any_", paste0("status", 0:28)),
  "post_pfmed" <- paste0("post_pfmed_", paste0("status", 0:28)),
  "post_pfmedid" <- paste0("post_pfmedid_", paste0("status", 0:28)),
  "post_any_pfid" <- paste0("post_any_pfid_", paste0("status", 0:28)),
  "post_date_pfid" <- paste0("post_date_pfid_", paste0("status", 0:28))
)

# Check that all names defined in data_extractions are in df df_med_status
# all(unlist(selected_variables_list) %in% names(df_med_status))

print("Define variable names successfully")

dfs_med_status_summary <- list()

for (selected_variables in seq_along(selected_variables_list)) {

  print(paste0("Run ", selected_variables, ":"))
  # Restructure data into 'long' format
  dfs_med_status_long_tmp <- df_med_status %>%
    dplyr::select(dplyr::all_of(selected_variables_list[[selected_variables]])) %>%
    tidyr::pivot_longer(
      cols = c(dplyr::all_of(selected_variables_list[[selected_variables]])),
      names_to = c("time", "selected_codes", "med_status"),
      names_sep = "_"
    )

  print("- Pivot data successfully")

  dfs_med_status_summary[[selected_variables]] <- dfs_med_status_long_tmp %>%
    dplyr::group_by(time, selected_codes, med_status) %>%
    dplyr::mutate(n = sum(value, na.rm = TRUE)) %>%
    dplyr::ungroup() %>%
    dplyr::select(time, selected_codes, med_status, n) %>%
    dplyr::distinct() %>%
    dplyr::filter(n > 7) %>%
    dplyr::mutate(n = round(n, -1))

  rm(dfs_med_status_long_tmp)
  gc()

  print("- Calculate sums successfully")
}

# Combine all data frames
df_med_status_summary <- purrr::map_dfr(dfs_med_status_summary, dplyr::bind_rows)

print("Combine dataframes successfully")

# Write summary file
readr::write_csv(
  df_med_status_summary,
  here::here("output", "data_development", "med_status_counts.csv")
)

print("Write successfully")
