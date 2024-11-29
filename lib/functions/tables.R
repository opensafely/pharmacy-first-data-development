#  Create top 5 table grouped by pharmacy_first_med status
#  Data needs to have the following columns:
#  pharmacy_first_med
#  term
#  count
#  ratio_by_group
gt_top_meds <- function(data) {
  data |>
    gt(
      groupname_col = "pharmacy_first_med",
      rowname_col = "term"
    ) %>%
    tab_header(
      title = "Top 5 medications linked to Pharmacy First consultations",
      subtitle = "Timeframe: 1st Feb 2024 to 31st July 2024"
    ) %>%
    cols_label(
      term = md("**Medication**"),
      count = md("**Count**"),
      ratio_by_group = md("**%**")
    ) %>%
    fmt_number(
      columns = count,
      decimals = 0
    ) %>%
    fmt_percent(
      columns = ratio_by_group,
      decimals = 1
    ) %>%
    tab_style(
      style = cell_text(weight = "bold"),
      locations = cells_row_groups(groups = everything())
    ) %>%
    tab_stub_indent(
      rows = everything(),
      indent = 3
    )
}
