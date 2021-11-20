task :clean do
  sh('rm -rf _site')
end

task :deep_clean => [:clean] do
  sh('rm -rf gems')
end

task :dependencies do
  sh('bundle install --path gems')
end

file '_sass/brand/.git' do
  sh('git submodule update --init')
end

task :submodules => ['_sass/brand/.git']

task :dev => [:dependencies, :submodules] do
  sh('bundle exec jekyll serve --drafts')
end

task :build => [:dependencies, :submodules] do
  sh('bundle exec jekyll build')
end

task :validate => [:build] do
  # Explanation of arguments:
  # --assume-extension  # Tells html-proofer that `.html` files can be accessed without the `.html` part in the url.
  # --disable-external  # For speed. Ideally we'd check external links too, but ignoring for now.
  # --empty-alt-ignore  # To avoid needing to fix lots upfront, we can migrate towards this later.
  # --allow-hash-href   # Allow empty `#` links to mean "top of page". It's true that these can be errors, however we have far too many to really address this.
  # --url-swap          # Adjust for Jekyll's baseurl. See https://github.com/gjtorikian/html-proofer/issues/618 for more.
  sh('bundle exec htmlproofer _site --assume-extension --disable-external --empty-alt-ignore --url-swap "^/style/:/"')
end
