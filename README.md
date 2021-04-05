# ZFS Time Machine

Zero conf ZFS snapshot daemon

## One Conf

Ok, just mark the datasets that you want to keep

```sh
zfs set time-machine:status=on <dataset>
```

## Schedule

```txt
< 24h: hourly
< 30d: daily
< 1y: weekly
> 1y: monthly
```

```
pip3 install -U https://github.com/ms-jpq/zfs_time_machine/archive/t1000.tar.gz
```
