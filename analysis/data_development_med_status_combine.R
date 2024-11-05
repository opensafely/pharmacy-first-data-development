library(magrittr)

df_med_status_pre_summary <- readr::read_csv(
  here::here("output", "data_development", "med_status_pre_counts.csv")
)

df_med_status_post_summary <- readr::read_csv(
  here::here("output", "data_development", "med_status_post_counts.csv")
)

df_med_status_summary <- rbind(df_med_status_pre_summary, df_med_status_post_summary)

readr::write_csv(
  df_med_status_summary,
  here::here("output", "data_development", "med_status_counts.csv")
)
