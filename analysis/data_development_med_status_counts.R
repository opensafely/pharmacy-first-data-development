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
  "post_any" <- paste0("post_any_", paste0("status", 0:28)),
  "post_pfmed" <- paste0("post_pfmed_", paste0("status", 0:28)),
  "post_pfmedid" <- paste0("post_pfmedid_", paste0("status", 0:28))
)

# Check that all names defined in data_extractions are in df df_med_status
all(unlist(selected_variables_list) %in% names(df_med_status))

print("Define variable names successfully")

dfs_med_status_long <- list()

for (selected_variables in seq_along(selected_variables_list)) {
  # Restructure data into 'long' format
  dfs_med_status_long[[selected_variables]] <- df_med_status %>%
    dplyr::select(dplyr::all_of(selected_variables_list[[selected_variables]])) %>%
    tidyr::pivot_longer(
      cols = c(dplyr::all_of(selected_variables_list[[selected_variables]])),
      names_to = c("time", "selected_codes", "med_status"),
      names_sep = "_"
    )

  print(paste0("Pivot data successfully, run: ", selected_variables))
}

dfs_med_status_summary <- list()

for (df_med_status_long in seq_along(dfs_med_status_long)) {
  # Calculate sum and apply statistical disclosure control
  dfs_med_status_summary[[df_med_status_long]] <- dfs_med_status_long[[df_med_status_long]] %>%
    dplyr::group_by(time, selected_codes, med_status) %>%
    dplyr::mutate(n = sum(value, na.rm = TRUE)) %>%
    dplyr::ungroup() %>%
    dplyr::select(time, selected_codes, med_status, n) %>%
    dplyr::distinct() %>%
    dplyr::filter(n > 7) %>%
    dplyr::mutate(n = round(n, -1))

  print(paste0("Calculate sums successfully, run: ", df_med_status_long))
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
