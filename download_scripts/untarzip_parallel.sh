export LOCAL_DIR="/your/local/path/to/root"
cd $LOCAL_DIR
my_func() {
    tar xzf $1
}
for subj in {01..10}; do
my_func $LOCAL_DIR/sub-${subj}.tar.gz &
done
wait
echo "Finished un tarzipping for all subjects in the loop"