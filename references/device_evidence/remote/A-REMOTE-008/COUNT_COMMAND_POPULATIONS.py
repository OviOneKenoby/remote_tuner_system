"""Read compilation databases; distinguish contexts from unique source files."""
import collections
import json
import sys
from pathlib import Path

for filename in sys.argv[1:]:
    entries = json.loads(Path(filename).read_text())
    identities = {(Path(x['directory']) / x['file']).resolve() for x in entries}
    boot = sum('/bootloader/' in x['output'].replace('\\', '/').lower()
               for x in entries)
    print(json.dumps({
        'database': filename,
        'compilation_contexts': len(entries),
        'unique_source_files': len(identities),
        'command_types_by_source_suffix': dict(collections.Counter(
            Path(x['file']).suffix.lower() for x in entries)),
        'application_contexts': len(entries) - boot,
        'bootloader_contexts': boot,
        'link_actions_in_population': 0,
    }, indent=2))
