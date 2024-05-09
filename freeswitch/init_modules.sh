#!/bin/bash
pushd . >/dev/null
SCRIPT_PATH="${BASH_SOURCE[0]}"
while ([ -h "${SCRIPT_PATH}" ]); do
  cd "$(dirname "${SCRIPT_PATH}")"
  SCRIPT_PATH="$(readlink "$(basename "${SCRIPT_PATH}")")"
done
cd "$(dirname "${SCRIPT_PATH}")" >/dev/null
SCRIPT_PATH="$(pwd)"
popd >/dev/null

(rm -fr $SCRIPT_PATH/.modules/freeswitch/* $SCRIPT_PATH/.modules/freeswitch/.*) >/dev/null 2>&1 || true
(rm -fr $SCRIPT_PATH/.modules/freeswitch-modules/* $SCRIPT_PATH/.modules/freeswitch-modules/.*) >/dev/null 2>&1 || true

set -e

git clone -bv1.10.11 --depth 1 https://github.com/signalwire/freeswitch.git "$SCRIPT_PATH/.modules/freeswitch" >/dev/null
git clone -b1.2.11 --depth 1 https://github.com/jambonz/freeswitch-modules.git "$SCRIPT_PATH/.modules/freeswitch-modules" >/dev/null
for MODULE in $(ls -1 $SCRIPT_PATH/.modules/freeswitch-modules | egrep '^mod_'); do
  cp -fr "$SCRIPT_PATH/.modules/freeswitch-modules/$MODULE" "$SCRIPT_PATH/.modules/freeswitch/src/mod/applications/$MODULE"
done
