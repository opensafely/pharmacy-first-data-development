library(magrittr)
library(data.table)

# Load data
df_med_status <- readr::read_csv(
  here::here("output", "data_development", "med_status_data_development.csv.gz")
)

# Convert data frame to data.table
setDT(df_med_status)

# Extract all variables to be rechaped into long format
med_status_count_var_names <- names(df_med_status)[2:length(names(df_med_status))]

# Restructure data into 'long' format
df_med_status_tidy <- melt(
  df_med_status,
  id_.vars = "patient_id",
  measure.vars = med_status_count_var_names,
  variable.name = "variable",
  value.name = "value"
)

df_med_status_tidy[, c("time", "selected_codes", "med_status") := tstrsplit(variable, "_")][, variable := NULL]

# Convert to tibble
df_med_status_tidy <- tibble::as_tibble(df_med_status_tidy)

# Calculate sum and apply statistical disclosure control
df_med_status_summary <- df_med_status_tidy %>%
  dplyr::group_by(time, selected_codes, med_status) %>%
  dplyr::mutate(n = sum(value, na.rm = TRUE)) %>%
  dplyr::ungroup() %>%
  dplyr::select(time, selected_codes, med_status, n) %>%
  dplyr::distinct() %>%
  dplyr::filter(n > 7) %>%
  dplyr::mutate(n = round(n, -1))

# Write summary file
readr::write_csv(
  df_med_status_summary,
  here::here("output", "data_development", "med_status_counts.csv")
)
