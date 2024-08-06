# Build the Haskell application
FROM fpco/stack-build:lts-15.4 as haskell

# Tell `stack` where to find its content (not in $HOME)
ENV STACK_ROOT /home/stackage/.stack

WORKDIR /opt/build
COPY main.hs .
RUN stack ghc --package process -- main.hs

# Switch Ubuntu back to Alpine
FROM alpine:latest

# Add the libraries we need to run the application
RUN apk add libc6-compat gmp

COPY --from=haskell /opt/build/main /main
CMD ["sh", "-c", "sleep 999999999"]