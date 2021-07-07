"""
Copyright (C) 2015-2020  Red Hat, Inc. <http://www.redhat.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Test desciption:
    Testing Volume Type Change from replicated to
    Arbitered volume
@runs_on([['replicated', 'distributed-replicated'],
          ['glusterfs', 'nfs', 'cifs']])
"""

# disruptive;rep
# TODO: nfs and cifs to be added

from tests.d_parent_test import DParentTest


class TestCase(DParentTest):

    # def _wait_for_untar_completion(self):
    #     """Wait for untar to complete"""
    #     has_process_stopped = []
    #     for proc in self.io_process:
    #         try:
    #             ret, _, _ = proc.async_communicate()
    #             if not ret:
    #                 has_process_stopped.append(False)
    #             has_process_stopped.append(True)
    #         except ValueError:
    #             has_process_stopped.append(True)
    #     return all(has_process_stopped)

    # def _convert_replicated_to_arbiter_volume(self):
    #     """
    #     Helper module to convert replicated to arbiter volume.
    #     """
    #     # pylint: disable=too-many-statements
    #     # Remove brick to reduce the replica count from replica 3
    #     g.log.info("Removing bricks to form replica 2 volume")
    #     ret = shrink_volume(self.mnode, self.volname, replica_num=0)
    #     self.assertTrue(ret, "Failed to remove brick on volume %s"
    #                     % self.volname)
    #     g.log.info("Successfully removed brick on volume %s", self.volname)

    #     # Wait for volume processes to be online
    #     g.log.info("Wait for volume processes to be online")
    #     ret = wait_for_volume_process_to_be_online(self.mnode, self.volname)
    #     self.assertTrue(ret, "Volume %s process not online despite waiting "
    #                          "for 300 seconds" % self.volname)
    #     g.log.info("Successful in waiting for volume %s processes to be "
    #                "online", self.volname)

    #     # Verifying all bricks online
    #     g.log.info("Verifying volume's all process are online")
    #     ret = verify_all_process_of_volume_are_online(self.mnode, self.volname)
    #     self.assertTrue(ret, "Volume %s : All process are not online"
    #                     % self.volname)
    #     g.log.info("Volume %s : All process are online", self.volname)

    #     # Adding the bricks to make arbiter brick
    #     g.log.info("Adding bricks to convert to Arbiter Volume")
    #     replica_arbiter = {'replica_count': 1, 'arbiter_count': 1}
    #     ret = expand_volume(self.mnode, self.volname, self.servers,
    #                         self.all_servers_info, force=True,
    #                         **replica_arbiter)
    #     self.assertTrue(ret, "Failed to expand the volume  %s" % self.volname)
    #     g.log.info("Changing volume to arbiter volume is successful %s",
    #                self.volname)

    #     # Wait for volume processes to be online
    #     g.log.info("Wait for volume processes to be online")
    #     ret = wait_for_volume_process_to_be_online(self.mnode, self.volname)
    #     self.assertTrue(ret, "Failed to wait for volume %s processes "
    #                          "to be online" % self.volname)
    #     g.log.info("Successful in waiting for volume %s processes to be "
    #                "online", self.volname)

    #     # Verify volume's all process are online
    #     g.log.info("Verifying volume's all process are online")
    #     ret = verify_all_process_of_volume_are_online(self.mnode, self.volname)
    #     self.assertTrue(ret, "Volume %s : All process are not online"
    #                     % self.volname)
    #     g.log.info("Volume %s : All process are online", self.volname)

    def test_replica_to_arbiter_volume_with_io(self):
        """
        Description: Replica 3 to arbiter conversion with ongoing IO's

        Steps :
        1) Create a replica 3 volume and start volume.
        2) Set client side self heal off.
        3) Fuse mount the volume.
        4) Create directory dir1 and write data.
           Example: untar linux tar from the client into the dir1
        5) When IO's is running, execute remove-brick command,
           and convert replica 3 to replica 2 volume
        6) Execute add-brick command and convert to arbiter volume,
           provide the path of new arbiter brick.
        7) Issue gluster volume heal.
        8) Heal should be completed with no files in split-brain.
        """

        # pylint: disable=too-many-statements
        self.subvols = get_subvols(self.mnode, self.volname)['volume_subvols']
        # self._convert_replicated_to_arbiter_volume()
        # Create a dir to start untar
        self.linux_untar_dir = "{}/{}".format(self.mounts[0].mountpoint,
                                              "linuxuntar")
        ret = mkdir(self.clients[0], self.linux_untar_dir)
        self.assertTrue(ret, "Failed to create dir linuxuntar for untar")

        # Start linux untar on dir linuxuntar
        self.io_process = run_linux_untar(self.clients[0],
                                          self.mounts[0].mountpoint,
                                          dirs=tuple(['linuxuntar']))
        self.is_io_running = True

        # Convert relicated to arbiter volume
        self._convert_replicated_to_arbiter_volume()

        # Wait for IO to complete.
        ret = self._wait_for_untar_completion()
        self.assertFalse(ret, "IO didn't complete or failed on client")
        self.is_io_running = False

        # Start healing
        ret = trigger_heal(self.mnode, self.volname)
        self.assertTrue(ret, 'Heal is not started')
        g.log.info('Healing is started')

        # Monitor heal completion
        ret = monitor_heal_completion(self.mnode, self.volname,
                                      timeout_period=3600)
        self.assertTrue(ret, 'Heal has not yet completed')

        # Check if heal is completed
        ret = is_heal_complete(self.mnode, self.volname)
        self.assertTrue(ret, 'Heal is not complete')
        g.log.info('Heal is completed successfully')

        # Check for split-brain
        ret = is_volume_in_split_brain(self.mnode, self.volname)
        self.assertFalse(ret, 'Volume is in split-brain state')
        g.log.info('Volume is not in split-brain state')
