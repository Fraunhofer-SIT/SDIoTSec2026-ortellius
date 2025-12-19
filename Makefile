knowledge_base/shadow_maps.tar.gz: knowledge_base/memory_maps.tar.gz
	python3 -m tools.svdmap make-shadows $< $@

knowledge_base/shadow_maps_%.tar.gz: knowledge_base/memory_maps_%.tar.gz
	python3 -m tools.svdmap make-shadows $< $@

knowledge_base/memory_maps.tar.gz: knowledge_base/svds.tar.gz
	mkdir tmp
	tar xf $< -C tmp
	python3 -m tools.svdmap ingest tmp $@
	rm -rf tmp

knowledge_base/memory_maps_%.tar.gz: knowledge_base/svds.tar.gz
	mkdir tmp
	tar xf $< -C tmp
	python3 -m tools.svdmap ingest tmp/svds/$* $@
	rm -rf tmp

knowledge_base/svds.tar.gz:
	tools/collect_svds.sh
	mv svds.tar.gz knowledge_base/svds.tar.gz