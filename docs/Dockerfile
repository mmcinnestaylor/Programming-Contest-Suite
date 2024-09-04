FROM ruby:latest

RUN gem install bundler

WORKDIR /usr/src/app

COPY . .

RUN bundle install

EXPOSE 4000

ENTRYPOINT [ "bundle", "exec", "jekyll" ]
CMD [ "serve", "--incremental", "--host=0.0.0.0" ]
