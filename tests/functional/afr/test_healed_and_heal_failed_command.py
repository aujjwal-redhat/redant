"""
Copyright (C) 2020 Red Hat, Inc. <http://www.redhat.com>

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

@runs_on([['replicated'], ['glusterfs', 'nfs']])
"""

# disruptive;rep
# TODO: nfs

# from random import choice
from tests.d_parent_test import DParentTest

class TestCase(DParentTest):
    
    def run_test(self, redant):
        """
        Description: Validate absence of `healed` and `heal-failed` options

        Steps:
        - Create and mount a replicated volume
        - Kill one of the bricks and write IO from mount point
        - Verify `gluster volume heal <volname> info healed` and `gluster
          volume heal <volname> info heal-failed` command results in error
        - Validate `gluster volume help` doesn't list `healed` and
          `heal-failed` commands
        """

        # client, m_point = (self.mounts[0].client_system,
        #                    self.mounts[0].mountpoint)

        # # Kill one of the bricks in the volume
        # brick_list = get_online_bricks_list(self.mnode, self.volname)
        # self.assertIsNotNone(brick_list, 'Unable to get online bricks list')
        # ret = bring_bricks_offline(self.volname, choice(brick_list))
        # self.assertTrue(ret, 'Unable to kill one of the bricks in the volume')

        # # Fill IO in the mount point
        # cmd = ('/usr/bin/env python {} '
        #        'create_deep_dirs_with_files --dir-depth 10 '
        #        '--fixed-file-size 1M --num-of-files 50 '
        #        '--dirname-start-num 1 {}'.format(self.script_path, m_point))
        # ret, _, _ = g.run(client, cmd)
        # self.assertEqual(ret, 0, 'Not able to fill directory with IO')

        # # Verify `gluster volume heal <volname> info healed` results in error
        # cmd = 'gluster volume heal <volname> info'
        # ret, _, err = heal_info_healed(self.mnode, self.volname)
        # self.assertNotEqual(ret, 0, '`%s healed` should result in error' % cmd)
        # self.assertIn('Usage', err, '`%s healed` should list `Usage`' % cmd)

        # # Verify `gluster volume heal <volname> info heal-failed` errors out
        # ret, _, err = heal_info_heal_failed(self.mnode, self.volname)
        # self.assertNotEqual(ret, 0,
        #                     '`%s heal-failed` should result in error' % cmd)
        # self.assertIn('Usage', err,
        #               '`%s heal-failed` should list `Usage`' % cmd)

        # # Verify absence of `healed` nd `heal-failed` commands in `volume help`
        # cmd = 'gluster volume help | grep -i heal'
        # ret, rout, _ = g.run(self.mnode, cmd)
        # self.assertEqual(
        #     ret, 0, 'Unable to query help content from `gluster volume help`')
        # self.assertNotIn(
        #     'healed', rout, '`healed` string should not exist '
        #     'in `gluster volume help` command')
        # self.assertNotIn(
        #     'heal-failed', rout, '`heal-failed` string should '
        #     'not exist in `gluster volume help` command')
