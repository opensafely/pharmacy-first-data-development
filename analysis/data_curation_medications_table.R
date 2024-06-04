library(magrittr)

# Load data
df_medications <- readr::read_csv(
  here::here("output", "data_curation", "data_curation.csv.gz"),
  col_types = list(
    pre_first_medication_status = "c",
    post_first_medication_status = "c"
  )
) %>%
  dplyr::select(
    pre_first_medication_status, post_first_medication_status
  )

# Reshape data
df_medications_tidy <- df_medications %>%
  tidyr::pivot_longer(
    cols = c(
      "pre_first_medication_status",
      "post_first_medication_status"
    ),
    names_to = c("time", "variable"),
    names_sep = "(?<=pre|post)"
  ) %>%
  dplyr::mutate(variable = stringr::str_sub(variable, 2, -1))

# Count dmd_code and medication_status pre and post
df_medications_summary <- df_medications_tidy %>%
  dplyr::group_by(time, variable) %>%
  tidyr::nest() %>%
  dplyr::mutate(counts = purrr::map(data, dplyr::count, value)) %>%
  dplyr::select(-data) %>%
  tidyr::unnest(counts) %>%
  dplyr::arrange(variable, dplyr::desc(time)) %>%
  dplyr::mutate(n = round(n, -1)) %>%
  dplyr::filter(n >= 10)

# Write summary file
readr::write_csv(
  df_medications_summary,
  here::here("output", "data_curation", "medication_status_counts.csv")
)
