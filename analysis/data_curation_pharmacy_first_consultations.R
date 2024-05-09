library(magrittr)

# Load data
df_consultations <- readr::read_csv(
  here::here("output", "data_curation", "data_curation.csv.gz"),
  col_types = list(
    pre_count_distinct_consultations = "i",
    post_count_distinct_consultations = "i",
    pre_count_comm_pharm_bp_service = "i",
    post_count_comm_pharm_bp_service = "i",
    pre_count_comm_pharm_contraception_service = "i",
    post_count_comm_pharm_contraception_service = "i",
    pre_count_comm_pharm_consultation_service = "i",
    post_count_comm_pharm_consultation_service = "i",
    pre_count_pharm_first_service = "i",
    post_count_pharm_first_service = "i"
  )
) %>% dplyr::select(
  pre_count_distinct_consultations,
  post_count_distinct_consultations,
  pre_count_comm_pharm_bp_service,
  post_count_comm_pharm_bp_service,
  pre_count_comm_pharm_contraception_service,
  post_count_comm_pharm_contraception_service,
  pre_count_comm_pharm_consultation_service,
  post_count_comm_pharm_consultation_service,
  pre_count_pharm_first_service,
  post_count_pharm_first_service
)

df_consultations_tidy <- df_consultations %>%
  tidyr::pivot_longer(
    cols = c(
      "pre_count_distinct_consultations",
      "post_count_distinct_consultations",
      "pre_count_comm_pharm_bp_service",
      "post_count_comm_pharm_bp_service",
      "pre_count_comm_pharm_contraception_service",
      "post_count_comm_pharm_contraception_service",
      "pre_count_comm_pharm_consultation_service",
      "post_count_comm_pharm_consultation_service",
      "pre_count_pharm_first_service",
      "post_count_pharm_first_service"
    ),
    names_to = c("time", "variable"),
    names_sep = "(?<=pre|post)"
  ) %>%
  dplyr::mutate(variable = stringr::str_sub(variable, 2, -1))

df_consultations_summary <- df_consultations_tidy %>%
  dplyr::group_by(time, variable) %>%
  dplyr::count() %>%
  dplyr::arrange(variable, dplyr::desc(time)) %>%
  dplyr::mutate(n = round(n, -1)) %>%
  dplyr::filter(n >= 10)

# Write summary file
readr::write_csv(
  df_consultations_summary,
  here::here("output", "data_curation", "consultations_counts.csv")
)
