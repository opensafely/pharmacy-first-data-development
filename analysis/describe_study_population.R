library(dplyr)
library(tidyr)
library(readr)
library(arrow)
library(here)
library(fs)

dataset <- read_feather(
  here("output", "study_population", "study_population.arrow")
)

redact_and_round <- function(x) {
  if_else(x <= 7, 0, round(x / 5) * 5)
}

counts <- dataset |>
  pivot_longer(
    starts_with("practice_"),
    names_to = "time_point",
    names_prefix = "practice_",
    values_to = "practice_pseudo_id"
  ) |>
  filter(!is.na(practice_pseudo_id)) |>
  summarise(
    n_patients = n_distinct(patient_id),
    n_practices = n_distinct(practice_pseudo_id),
    .by = time_point
  ) |>
  mutate(across(c(n_patients, n_practices), redact_and_round))

dir_create(here("output", "study_population"))
write_csv(
  counts,
  here("output", "study_population", "study_population_summary.csv")
)
