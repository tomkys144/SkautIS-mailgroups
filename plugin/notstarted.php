<?php
$unit = $domain = '';
echo ('<form action="send.php" method="post">
                <table>
                    <tr>
                        <td>Jednotka:</td>
                        <td><input type = "text" name = "unit"></td>
                    </tr>

                    <tr>
                        <td>Doména:</td>
                        <td><input type = "text" name = "domain"></td>
                    </tr>
                </table>
                <input type="submit" name="Start">
            </form>');