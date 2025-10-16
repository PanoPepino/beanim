from manim_beanim import extract_citation, extract_equations

extract_citation(
    bib_file="example_extract_ref_equation/latex_to_extract/refs_example.bib",  # .bib file to extract references from
    # your family name if your want to change it for your initials (common practice in theoretical physics community)
    your_family_name="Perico",
    initials="PP",  # your initials that will substitute your whole name in the citation above
    output_file_name="example_extract_ref_equation/dictionaries_extracted/refs.txt"
    # output directory and name of the .txt file to contain the dictionary

)

extract_equations(
    tex_file="example_extract_ref_equation/latex_to_extract/latex_example.tex",  # .tex file to extract equations from
    output_file="example_extract_ref_equation/dictionaries_extracted/equations.txt",
    # output directory and name of the .txt file to contain the dictionary
)
