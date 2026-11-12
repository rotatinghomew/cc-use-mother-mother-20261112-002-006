测试：python3 -m unittest discover -s tests/transfer_missions -p 'test_*.py'
构建：python3 -m compileall -q vulnerable_transfer_planner tests/transfer_missions
验收：python3 -m vulnerable_transfer_planner.fieldwork.command fixtures/demo.json --database /tmp/vulnerable_transfer_planner-acceptance.sqlite3
