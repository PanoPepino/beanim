from beanim import extract_citation, extract_equations

extract_citation(
    bib_file="example_refeq/latex/test_ref.bib",
    your_family_name="Panizo",
    initials="DP",
    output_file_name="example_refeq/dictionaries/test_ref.txt",
)

extract_equations(
    tex_file="example_refeq/latex/test_file.tex",
    output_file="example_refeq/dictionaries/eq_test_file.txt",
)
