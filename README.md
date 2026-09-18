# Yinzhe Zhou — personal website

A GitHub Pages / Jekyll personal site with a restrained light-blue design.

## Editing

- `index.html`: homepage introduction, education, and photography link.
- `_layouts/personal.html`: shared navigation, metadata, and footer.
- `assets/css/personal.css`: responsive styles for the personal pages.
- `_data/research.yml`: research title, author position, and internship dates. This is shared by the homepage, Research page, and CV.
- `_data/cv.yml`: education, internships, academic research, honors, and skills shared by the homepage, Research page, and CV.
- `_pages/cv.html`: CV page layout.
- `assets/docs/Yinzhe_CV.pdf`: downloadable CV compiled from the current Overleaf resume.
- `_pages/photo-2025.md`: film gallery, using existing images and thumbnails.
- `_data/navigation.yml`: navigation links.

The CV content is synchronized with the Overleaf resume as of September 2026. HACo is listed as an unpublished manuscript with co-first authorship. The author has approved sharing the technical contributions and results from the resume; the paper itself is not hosted here.

## Local development

With Ruby 3.3 and Bundler (the locally verified runtime):

```sh
bundle install
bundle exec jekyll serve
```

The existing Minimal Mistakes remote theme remains available for archive and utility pages. Main personal pages use the local `personal` layout, which does not need JavaScript or external fonts.
