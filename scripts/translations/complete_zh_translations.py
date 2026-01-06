#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and
# limitations under the License.

"""
Script to complete missing Chinese translations in messages.po file.
This script uses babel to parse the PO file and provides translations
for untranslated entries using AI or translation mappings.
"""

import sys
from pathlib import Path
from babel.messages import catalog, pofile

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent
PO_FILE = BASE_DIR / "superset" / "translations" / "zh" / "LC_MESSAGES" / "messages.po"


def translate_string(msgid: str) -> str:
    """
    Translate a string to Chinese.
    This is a placeholder - in practice, you might want to use an AI translation service
    or maintain a comprehensive translation dictionary.
    """
    # Keep original for matching, but also try stripped version
    msgid_original = msgid
    msgid_clean = msgid.strip()
    
    # Common translations dictionary
    translations = {" at line %(line)d": "在第 %(line)d 行",
        " near '%(highlight)s'": "在 '%(highlight)s' 附近",
        " source code of Superset's sandboxed parser": "Superset 沙箱解析器的源代码",
        " to mark a column as a time column": "以将列标记为时间列",
        " to visualize your data.": "以可视化您的数据。",
        "%(label)s file": "%(label)s 文件",
        "%(name)s.csv": "%(name)s.csv",
        "%(name)s.pdf": "%(name)s.pdf",
        "%(prefix)s %(title)s": "%(prefix)s %(title)s",
        "%(report_type)s schedule frequency exceeding limit. Please configure a schedule with a minimum interval of %(minimum_interval)d minutes per execution.": "%(report_type)s 计划频率超过限制。请配置一个每次执行最少间隔 %(minimum_interval)d 分钟的计划。",
        "%s items could not be tagged because you don't have edit permissions to all selected objects.": "%s 个项目无法标记，因为您没有对所有选定对象的编辑权限。",
        "%s items could not be tagged because you don't have edit permissions to all selected objects.": "%s 个项目无法标记，因为您没有对所有选定对象的编辑权限。",  # 带右单引号版本
        "+ %s more": "+ 还有 %s 个",
        "... and %s others": "... 以及其他 %s 个",
        "10000": "10000",
        "1AS": "1AS",
        "1D": "1天",
        "1H": "1小时",
        "1M": "1分钟",
        "1W": "1周",
        "1Y": "1年",
        "1m": "1个月",
        "1s": "1秒",
        "1w": "1周",
        "1y": "1年",
        "1T": "1T",
        "22": "22",
        "3D": "3天",
        "4 weeks (freq=4W-MON)": "4周（频率=4W-MON）",
        "7D": "7天",
        "A database port is required when connecting via SSH Tunnel.": "通过 SSH 隧道连接时需要数据库端口。",
        "A date is required when using custom date shift": "使用自定义日期偏移时需要日期",
        "A dictionary with column names and their data types if you need to change the defaults. Example: {\"user_id\":\"int\"}. Check Python's Pandas library for supported data types.": "如果需要更改默认值，请提供列名及其数据类型的字典。例如：{\"user_id\":\"int\"}。请查看 Python 的 Pandas 库以了解支持的数据类型。",
        "A handlebars template that is applied to the data": "应用于数据的 Handlebars 模板",
        "A list of domain names that can embed this dashboard. Leaving this field empty will allow embedding from any domain.": "可以嵌入此看板的域名列表。将此字段留空将允许从任何域嵌入。",
        "A map that takes rendering circles with a variable radius at latitude/longitude coordinates": "在地理坐标上渲染可变半径圆的地图",
        "A reusable dataset will be saved with your chart.": "可重用的数据集将与您的图表一起保存。",
        "A waterfall chart is a form of data visualization that helps in understanding\n          the cumulative effect of sequentially introduced positive or negative values.\n          These intermediate values can either be time based or category based.": "瀑布图是一种数据可视化形式，有助于理解\n          顺序引入的正值或负值的累积效果。\n          这些中间值可以是基于时间的或基于类别的。",
        "Add calculated temporal columns to dataset in \"Edit datasource\" modal": "在\"编辑数据源\"模态框中向数据集添加计算的时间列",
        "Add color for positive/negative change": "为正/负变化添加颜色",
        "Add metrics to dataset in \"Edit datasource\" modal": "在\"编辑数据源\"模态框中向数据集添加指标",
        "Added 1 new column to the virtual dataset": "向虚拟数据集添加了 1 个新列",
        "Added to 1 dashboard": "已添加到 1 个看板",
        "Adds color to the chart symbols based on the positive or negative change from the comparison value.": "根据与比较值的正/负变化为图表符号添加颜色。",
        "Adjust column settings such as specifying the columns to read, how duplicates are handled, column data types, and more.": "调整列设置，例如指定要读取的列、如何处理重复项、列数据类型等。",
        "Adjust how spaces, blank lines, null values are handled and other file wide settings.": "调整如何处理空格、空行、空值以及其他文件范围的设置。",
        "Aggregates data within the boundary of grid cells and maps the aggregated values to a dynamic color scale": "在网格单元格边界内聚合数据，并将聚合值映射到动态颜色比例",
        "Allow DDL and DML": "允许 DDL 和 DML",
        "Allow changing catalogs": "允许更改目录",
        "Allow the execution of DDL (Data Definition Language: CREATE, DROP, TRUNCATE, etc.) and DML (Data Manipulation Language: INSERT, UPDATE, DELETE, etc.) statements.": "允许执行 DDL（数据定义语言：CREATE、DROP、TRUNCATE 等）和 DML（数据操作语言：INSERT、UPDATE、DELETE 等）语句。",
        "Authorization needed": "需要授权",
        "Available Handlebars Helpers in Superset:": "Superset 中可用的 Handlebars 助手：",
        "Average (Mean)": "平均值（均值）",
        "Base layer map style. See Mapbox documentation: %s": "基础图层地图样式。请参阅 Mapbox 文档：%s",
        "Base slope": "基础斜率",
        "Based on what should series be ordered on the chart and legend": "基于什么对图表和图例中的系列进行排序",
        "Big Number with Time Period Comparison": "带时间段比较的大数字",
        "Bulk tag": "批量标记",
        "CSS applied to the chart": "应用于图表的 CSS",
        "Calculate from first step": "从第一步计算",
        "Calculate from previous step": "从上一步计算",
        "Cannot find the table (%s) metadata.": "找不到表 (%s) 的元数据。",
        "Cannot have multiple credentials for the SSH Tunnel": "SSH 隧道不能有多个凭据",
        "Category, Value and Percentage": "类别、值和百分比",
        "Chart type requires a dataset": "图表类型需要数据集",
        "Choose whether a country should be shaded by the metric, or assigned a color based on a categorical dimension.": "选择国家是否应根据指标着色，或根据分类维度分配颜色。",
        "Color will be shaded based the normalized (0% to 100%) value of a given cell against the other cells in the table.": "颜色将根据给定单元格相对于表中其他单元格的标准化（0% 到 100%）值进行着色。",
        "Compare results with other time periods.": "与其他时间段的结果进行比较。",
        "Compose multiple layers together to form complex visuals.": "将多个图层组合在一起以形成复杂的视觉效果。",
        "Configure the chart size for each zoom level": "为每个缩放级别配置图表大小",
        "Confirm the user's password": "确认用户密码",
        "Connect Google Sheet": "连接 Google 表格",
        "Copy SELECT statement": "复制 SELECT 语句",
        "Copy URL": "复制 URL",
        "Copy the current data": "复制当前数据",
        "Copy the name of the HTTP Path of your cluster.": "复制集群的 HTTP 路径名称。",
        "Could not resolve hostname: \"%(host)s\".": "无法解析主机名：\"%(host)s\"。",
        "Could not validate the user in the current session.": "无法验证当前会话中的用户。",
        "Create chart with dataset": "使用数据集创建图表",
        "Credentials uploaded": "凭据已上传",
        "Cross-filter will be applied to all of the charts that use this dataset.": "交叉过滤器将应用于使用此数据集的所有图表。",
        "Custom SQL fields cannot contain sub-queries.": "自定义 SQL 字段不能包含子查询。",
        "Custom column name (leave blank for default)": "自定义列名（留空使用默认值）",
        "Custom width of the screenshot in pixels": "截图的自定义宽度（像素）",
        "Customize chart metrics or columns with currency symbols as prefixes or suffixes. Choose a symbol from the dropdown or type a custom symbol.": "使用货币符号作为前缀或后缀自定义图表指标或列。从下拉菜单中选择符号或输入自定义符号。",
        "Customize data source, filters, and layout.": "自定义数据源、过滤器和布局。",
        "Cyclic dependency detected": "检测到循环依赖",
        "DB column %(col_name)s has unknown type: %(value_type)s": "数据库列 %(col_name)s 具有未知类型：%(value_type)s",
        "DD/MM format dates, international and European format": "DD/MM 格式日期，国际和欧洲格式",
        "Dark Cyan": "深青色",
        "Dashboard cannot be copied due to invalid parameters.": "由于参数无效，无法复制看板。",
        "Data URI is not allowed.": "不允许数据 URI。",
        "Database driver for importing maybe not installed. Visit the driver installation page for more information.": "可能未安装用于导入的数据库驱动程序。访问驱动程序安装页面了解更多信息。",
        "Database upload file failed, while saving metadata": "数据库上传文件失败，保存元数据时",
        "Dataset schema is invalid, caused by: %(error)s": "数据集架构无效，原因：%(error)s",
        "Datasource type is invalid": "数据源类型无效",
        "Day (freq=D)": "天（频率=D）",
        "Default URL to redirect to when accessing from the dataset list.": "从数据集列表访问时重定向到的默认 URL。",
        "Define delivery schedule, timezone, and frequency settings.": "定义交付计划、时区和频率设置。",
        "Define the database, SQL query, and triggering conditions for your alert.": "定义警报的数据库、SQL 查询和触发条件。",
        "Defines the grid size in pixels": "定义网格大小（像素）",
        "Defines the value that determines the boundary between different color ranges.": "定义确定不同颜色范围之间边界的值。",
        "Display percents in the label and tooltip as the percent of the total.": "在标签和工具提示中将百分比显示为总数的百分比。",
        "Download is on the way": "下载正在进行中",
        "Downloading %(rows)s rows based on the LIMIT configuration. It may take a while...": "根据 LIMIT 配置下载 %(rows)s 行。可能需要一些时间...",
        "Drill to detail is disabled for this database. Change the database settings to enable it.": "此数据库已禁用钻取到详细信息。更改数据库设置以启用它。",
        "Email subject name (optional)": "电子邮件主题名称（可选）",
        "Enter the unique project id for your database.": "输入数据库的唯一项目 ID。",
        "Enter the user's email": "输入用户的电子邮件",
        "Enter the user's username": "输入用户的用户名",
        "Excel file format cannot be determined": "无法确定 Excel 文件格式",
        "Fail login count": "登录失败次数",
        "Failed to execute %(query)s": "执行 %(query)s 失败",
        "Failed to generate chart edit URL": "生成图表编辑 URL 失败",
        "Failed to load chart data": "加载图表数据失败",
        "Failed to load chart data.": "加载图表数据失败。",
        "Failed to load dimensions for drill by": "加载钻取维度失败",
        "Featured color palettes": "精选调色板",
        "File extension is not allowed.": "不允许的文件扩展名。",
        "Filter only displays values relevant to selections made in other filters.": "过滤器仅显示与其他过滤器中的选择相关的值。",
        "Filters for values equal to this exact value.": "过滤等于此确切值的值。",
        "Filters for values less than or equal.": "过滤小于或等于的值。",
        "Form data not found in cache, reverting to chart metadata.": "在缓存中找不到表单数据，正在恢复为图表元数据。",
        "Form data not found in cache, reverting to dataset metadata.": "在缓存中找不到表单数据，正在恢复为数据集元数据。",
        "Format data labels. Use variables: {name}, {value}, {percent}": "格式化数据标签。使用变量：{name}、{value}、{percent}",
        "Give access to multiple catalogs in a single database connection.": "在单个数据库连接中提供对多个目录的访问。",
        "Go to the edit mode to configure the dashboard and add charts.": "进入编辑模式以配置看板并添加图表。",
        "Gold": "金色",
        "Green for increase, red for decrease": "绿色表示增加，红色表示减少",
        "Guest user cannot modify chart payload": "访客用户无法修改图表负载",
        "Hard value bounds applied for color coding.": "应用硬值边界进行颜色编码。",
        "How many buckets should the data be grouped in.": "数据应分为多少个桶。",
        "If changes are made to your SQL query, columns in your dataset may become unavailable. Adding a query with a `LIMIT` statement might help keep the dataset columns consistent.": "如果对 SQL 查询进行了更改，数据集中的列可能变得不可用。添加带有 `LIMIT` 语句的查询可能有助于保持数据集列的一致性。",
        "If enabled, this control sorts the results/values descending.": "如果启用，此控件将按降序对结果/值进行排序。",
        "In": "在",
        "In order to connect to non-public sheets you need to either provide a service account or make the sheet public.": "为了连接到非公共表格，您需要提供服务帐户或使表格公开。",
        "Inherit range from time filter": "从时间过滤器继承范围",
        "Insert Layer title": "插入图层标题",
        "Intensity is the value multiplied by the weight to obtain the final value.": "强度是值乘以权重以获得最终值。",
        "Invalid currency code in saved metrics": "保存的指标中的货币代码无效",
        "Invalid executor type": "执行器类型无效",
        "Invalid input": "无效输入",
        "Invalid permalink key": "无效的永久链接密钥",
        "Invalid reference to column: \"%(column)s\"": "对列的无效引用：\"%(column)s\"",
        "Invalid tab ids: %s(tab_ids)": "无效的标签页 ID：%s(tab_ids)",
        "JavaScript onClick href": "JavaScript onClick href",
        "Keep control settings?": "保留控件设置？",
        "Label for the index column. Don't use an existing column name.": "索引列的标签。不要使用现有的列名。",
        "Layer URL": "图层 URL",
        "Like": "类似",
        "Line charts on a map": "地图上的折线图",
        "List Roles": "列出角色",
        "List of n+1 values for bucketing metric into n buckets.": "用于将指标分桶为 n 个桶的 n+1 个值的列表。",
        "Make the x-axis categorical": "使 x 轴为分类轴",
        "Mark a column as temporal in \"Edit datasource\" modal": "在\"编辑数据源\"模态框中将列标记为时间列",
        "Match time shift color with original series": "使时间偏移颜色与原始系列匹配",
        "Max. features": "最大特征数",
        "Maximum number of features to fetch from service": "从服务获取的最大特征数",
        "Memory in bytes - binary (1024B => 1KiB)": "内存（字节）- 二进制（1024B => 1KiB）",
        "Memory in bytes - decimal (1024B => 1.024kB)": "内存（字节）- 十进制（1024B => 1.024kB）",
        "Memory transfer rate in bytes - binary (1024B => 1KiB/s)": "内存传输速率（字节）- 二进制（1024B => 1KiB/s）",
        "Memory transfer rate in bytes - decimal (1024B => 1.024kB/s)": "内存传输速率（字节）- 十进制（1024B => 1.024kB/s）",
        "Menu actions trigger": "菜单操作触发",
        "Metric ``%(metric_name)s`` not found in %(dataset_name)s.": "在 %(dataset_name)s 中找不到指标 ``%(metric_name)s``。",
        "Metric used as a weight for the grid's coloring": "用作网格着色的权重的指标",
        "Metric used to control height": "用于控制高度的指标",
        "Minimum must be strictly less than maximum": "最小值必须严格小于最大值",
        "Minimum radius size of the circle, in pixels. As the zoom level changes, this value is multiplied by the height metric to obtain the final radius in pixels.": "圆的最小半径大小（像素）。随着缩放级别的变化，此值乘以高度指标以获得最终的像素半径。",
        "Missing OAuth2 token": "缺少 OAuth2 令牌",
        "MotherDuck token": "MotherDuck 令牌",
        "Must provide credentials for the SSH Tunnel": "必须提供 SSH 隧道的凭据",
        "My beautiful colors": "我的美丽颜色",
        "No entities have this tag currently assigned": "当前没有实体分配此标签",
        "No form settings were maintained": "未保留表单设置",
        "No results match your filter criteria": "没有结果匹配您的过滤条件",
        "No validator found (configured for the engine)": "未找到验证器（为引擎配置）",
        "Not all required fields are complete. Please provide the following: %(fields)s": "并非所有必填字段都已完成。请提供以下内容：%(fields)s",
        "Number bounds used for color encoding from red to blue.": "用于从红色到蓝色颜色编码的数字边界。",
        "Number of periods to compare against. You can use negative numbers to compare to prior periods.": "要比较的周期数。您可以使用负数与之前的周期进行比较。",
        "Only applies when \"Label Type\" is not set to a percentage.": "仅在\"标签类型\"未设置为百分比时适用。",
        "Only applies when \"Label Type\" is set to show values.": "仅在\"标签类型\"设置为显示值时适用。",
        "Opacity of bubbles, 0 means completely transparent, 1 means completely opaque.": "气泡的不透明度，0 表示完全透明，1 表示完全不透明。",
        "Opacity, expects values between 0 and 100": "不透明度，期望值在 0 到 100 之间",
        "Orders the query result that generates the source data for the visualization.": "对生成可视化源数据的查询结果进行排序。",
        "Overlays a hexagonal grid on a map, and aggregates data within each hexagon.": "在地图上叠加六边形网格，并在每个六边形内聚合数据。",
        "Parameters related to the view and perspective on the map": "与地图上的视图和透视相关的参数",
        "Paste Private Key here": "在此处粘贴私钥",
        "Percentage difference between the time periods": "时间段之间的百分比差异",
        "Permissions successfully synced for %s": "已成功同步 %s 的权限",
        "Pick a dimension from which categorical colors are defined": "选择用于定义分类颜色的维度",
        "Pick a set of deck.gl charts to layer on top of one another.": "选择一组 deck.gl 图表以相互叠加。",
        "Pie charts on a map": "地图上的饼图",
        "Piecewise": "分段",
        "Please DO NOT overwrite the \"filter_scopes\" key.": "请不要覆盖 \"filter_scopes\" 键。",
        "Please choose a valid value": "请选择有效值",
        "Please confirm the overwrite values.": "请确认覆盖值。",
        "Please enter a valid email address": "请输入有效的电子邮件地址",
        "Please enter valid text. Spaces alone are not permitted.": "请输入有效文本。不允许仅使用空格。",
        "Please provide a valid range": "请提供有效范围",
        "Please provide a value within range": "请提供范围内的值",
        "Please re-export your file and try importing again": "请重新导出文件并再次尝试导入",
        "Please specify the Dataset ID for the ``%(name)s`` metric in the ``%(dataset_name)s`` dataset.": "请在 ``%(dataset_name)s`` 数据集中为 ``%(name)s`` 指标指定数据集 ID。",
        "Plot the distance (like flight paths) between origin and destination pairs.": "绘制起点和终点对之间的距离（如飞行路径）。",
        "Private Channels (Bot in channel)": "私有频道（频道中的机器人）",
        "Put positive values and valid minute and second value less than 60.": "输入正值和小于 60 的有效分钟和秒值。",
        "Radius in kilometers": "半径（公里）",
        "Recurring (every)": " recurring（每）",
        "Red for increase, green for decrease": "红色表示增加，绿色表示减少",
        "Redo the action": "重做操作",
        "Render HTML": "渲染 HTML",
        "Render columns in HTML format": "以 HTML 格式渲染列",
        "Renders table cells as HTML when applicable. For example, HTML links will become clickable.": "在适用时将表格单元格渲染为 HTML。例如，HTML 链接将变为可点击。",
        "Request Access": "请求访问",
        "Resource already has an attached report.": "资源已附加报告。",
        "Right-click on a dimension value to drill to detail by that value.": "右键单击维度值以按该值钻取到详细信息。",
        "Role was successfully created!": "角色已成功创建！",
        "Role was successfully duplicated!": "角色已成功复制！",
        "Running statement %(statement_num)s out of %(statement_count)s": "正在运行语句 %(statement_num)s，共 %(statement_count)s 个",
        "SHA": "SHA",
        "Satellite Streets": "卫星街道",
        "Scroll down to the bottom to enable overwriting changes.": "向下滚动到底部以启用覆盖更改。",
        "Select a time grain for the visualization. The grain is the time discrete unit you want to visualize, for example '1 year' or '1 month'.": "为可视化选择时间粒度。粒度是您想要可视化的时间离散单位，例如\"1 年\"或\"1 个月\"。",
        "Select an aggregation method to apply to the metric.": "选择要应用于指标的聚合方法。",
        "Select columns that will be displayed in the table. You can drag and drop column names to reorder.": "选择将在表中显示的列。您可以拖放列名以重新排序。",
        "Select shape for computing values. \"FIXED\" sets all zoom levels to the same size, \"DYNAMIC\" adjusts based on zoom.": "选择用于计算值的形状。\"FIXED\" 将所有缩放级别设置为相同大小，\"DYNAMIC\" 根据缩放进行调整。",
        "Set header rows and the number of rows to read or skip.": "设置标题行和要读取或跳过的行数。",
        "Set up basic details, such as name and description.": "设置基本详细信息，例如名称和描述。",
        "Sets the hierarchy levels of the chart. Each level is represented by a different color.": "设置图表的层次级别。每个级别由不同的颜色表示。",
        "Shift + Click to sort by multiple columns": "Shift + 单击以按多列排序",
        "Solid": "实心",
        "Something went wrong with embedded authentication. Check the logs for more details.": "嵌入式身份验证出现问题。查看日志以了解更多详细信息。",
        "Sort series in ascending order": "按升序对系列进行排序",
        "Specify name to CREATE TABLE AS schema in: public": "指定名称以在 public 中创建表 AS 架构",
        "Specify name to CREATE VIEW AS schema in: public": "指定名称以在 public 中创建视图 AS 架构",
        "Statement %(statement_num)s out of %(statement_count)s": "语句 %(statement_num)s，共 %(statement_count)s 个",
        "Subtotal": "小计",
        "Switch to the next tab": "切换到下一个标签页",
        "Switch to the previous tab": "切换到上一个标签页",
        "Sync Permissions": "同步权限",
        "Syncing permissions for %s": "正在同步 %s 的权限",
        "Syncing permissions for %s in the background": "正在后台同步 %s 的权限",
        "Syntax Error: %(qualifier)s input \"%(input)s\" expecting \"%(expected)s\"": "语法错误：%(qualifier)s 输入 \"%(input)s\" 期望 \"%(expected)s\"",
        "Tab schema is invalid, caused by: %(error)s": "标签页架构无效，原因：%(error)s",
        "Table already exists. You can change your 'if table already exists' strategy to 'append' or 'replace', or choose a different table name.": "表已存在。您可以将\"如果表已存在\"策略更改为\"追加\"或\"替换\"，或选择不同的表名。",
        "Text / Markdown": "文本 / Markdown",
        "The API response from %s does not match the IDatabaseTable interface.": "来自 %s 的 API 响应与 IDatabaseTable 接口不匹配。",
        "The GeoJsonLayer takes in GeoJSON formatted data and renders it as interactive polygons.": "GeoJsonLayer 接收 GeoJSON 格式的数据并将其渲染为交互式多边形。",
        "The Sankey chart visually tracks the movement and transformation of data through different stages or categories.": "桑基图直观地跟踪数据在不同阶段或类别中的移动和转换。",
        "The URL is missing the dataset_id or slice_id parameters.": "URL 缺少 dataset_id 或 slice_id 参数。",
        "The X-axis is not on the filters list": "X 轴不在过滤器列表中",
        "The X-axis is not on the filters list which will prevent it from being updated dynamically when the dashboard time range changes.": "X 轴不在过滤器列表中，这将阻止它在看板时间范围更改时动态更新。",
        "The column to be used as the source of the edge.": "用作边源的列。",
        "The column to be used as the target of the edge.": "用作边目标的列。",
        "The configuration for the map layers": "地图图层的配置",
        "The corner radius of the chart background": "图表背景的圆角半径",
        "The dataset column/metric that returns the values on your chart.": "返回图表上值的数据集列/指标。",
        "The dataset column/metric that returns the values on your chart. This can be the name of a column or a valid SQL aggregation expression.": "返回图表上值的数据集列/指标。这可以是列名或有效的 SQL 聚合表达式。",
        "The default catalog that should be used for the connection.": "连接应使用的默认目录。",
        "The default schema that should be used for the connection.": "连接应使用的默认架构。",
        "The exponent to compute all sizes from. \"EXP\" only": "用于计算所有大小的指数。仅 \"EXP\"",
        "The extent of the map on application start. FIT DATA automatically fits the extent to your data.": "应用程序启动时地图的范围。FIT DATA 自动将范围调整为您的数据。",
        "The following filters have the 'Select first filter value by default' option enabled.": "以下过滤器启用了\"默认选择第一个过滤器值\"选项。",
        "The function to use when aggregating points into groups.": "将点聚合为组时使用的函数。",
        "The height of the current zoom level to compute all heights from. \"LINEAR\" only": "用于计算所有高度的当前缩放级别的高度。仅 \"LINEAR\"",
        "The histogram chart displays the distribution of a dataset by showing the frequency of data points within consecutive, non-overlapping intervals, or bins.": "直方图通过显示连续、非重叠区间或箱内数据点的频率来显示数据集的分布。",
        "The lower limit of the threshold range of the Isoband": "Isoband 阈值范围的下限",
        "The name of the layer as described in GetCapabilities": "GetCapabilities 中描述的图层名称",
        "The result of this query must be a value capable of numeric representation.": "此查询的结果必须是能够进行数字表示的值。",
        "The result size exceeds the allowed limit.": "结果大小超过允许的限制。",
        "The row limit set for the chart was reached. The chart may not reflect all of the data.": "已达到为图表设置的行限制。图表可能无法反映所有数据。",
        "The schema of the submitted payload is invalid.": "提交的有效负载的架构无效。",
        "The screenshot could not be downloaded. Please, try again later.": "无法下载截图。请稍后再试。",
        "The screenshot is being generated. Please, do not leave the page.": "正在生成截图。请不要离开页面。",
        "The slope to compute all sizes from. \"LINEAR\" only": "用于计算所有大小的斜率。仅 \"LINEAR\"",
        "The upper limit of the threshold range of the Isoband": "Isoband 阈值范围的上限",
        "The user/password combination is not valid (Incorrect password for user %(username)s)": "用户/密码组合无效（用户 %(username)s 的密码不正确）",
        "The width of the current zoom level to compute all widths from. \"LINEAR\" only": "用于计算所有宽度的当前缩放级别的宽度。仅 \"LINEAR\"",
        "There are no components added to this tab": "此标签页没有添加组件",
        "This chart is managed externally, and can't be edited in Superset.": "此图表由外部管理，无法在 Superset 中编辑。",
        "This chart type is not supported when using an unsaved query.": "使用未保存的查询时不支持此图表类型。",
        "This control filters the whole chart based on the selected time range.": "此控件根据所选时间范围过滤整个图表。",
        "This controls whether the \"time_range\" field from the current dashboard context should be used as a default value.": "这控制是否应将当前看板上下文中的 \"time_range\" 字段用作默认值。",
        "This controls whether the time grain field from the current dashboard context should be used as a default value.": "这控制是否应将当前看板上下文中的时间粒度字段用作默认值。",
        "This dashboard is managed externally, and can't be edited in Superset.": "此看板由外部管理，无法在 Superset 中编辑。",
        "This database does not allow for DDL/DML, and the query could not be validated.": "此数据库不允许 DDL/DML，无法验证查询。",
        "This database is managed externally, and can't be edited in Superset.": "此数据库由外部管理，无法在 Superset 中编辑。",
        "This database table does not contain any data. Please select a table with data.": "此数据库表不包含任何数据。请选择包含数据的表。",
        "This dataset is managed externally, and can't be edited in Superset.": "此数据集由外部管理，无法在 Superset 中编辑。",
        "This dataset is not used to power any charts.": "此数据集不用于支持任何图表。",
        "This email is already associated with an account.": "此电子邮件已与帐户关联。",
        "This field is used as a unique identifier to attach the calculated columns to the dataset.": "此字段用作唯一标识符，用于将计算的列附加到数据集。",
        "This field is used as a unique identifier to attach the metrics to the dataset.": "此字段用作唯一标识符，用于将指标附加到数据集。",
        "This option has been disabled by the administrator.": "此选项已被管理员禁用。",
        "This page is intended to be embedded in an iframe, but it looks like it's not embedded correctly.": "此页面旨在嵌入在 iframe 中，但看起来它没有正确嵌入。",
        "This session has encountered an interruption, and some controls may not be saved.": "此会话遇到中断，某些控件可能无法保存。",
        "This username is already taken. Please choose another one.": "此用户名已被使用。请选择另一个。",
        "This will be applied to the whole table. Arrows (↑ and ↓) will indicate the sort direction.": "这将应用于整个表格。箭头（↑ 和 ↓）将指示排序方向。",
        "Time delta in natural language\n                  (example: '1 day ago', '2 weeks ago', '59 minutes ago', '3600 seconds ago')": "自然语言的时间增量\n                  （例如：'1 天前'、'2 周前'、'59 分钟前'、'3600 秒前'）",
        "To enable multiple column sorting, hold down the ⇧ Shift key and click on the columns you want to sort.": "要启用多列排序，请按住 ⇧ Shift 键并单击要排序的列。",
        "Total (%(aggfunc)s)": "总计（%(aggfunc)s）",
        "Total (%(aggregatorName)s)": "总计（%(aggregatorName)s）",
        "Treat values as categorical.": "将值视为分类。",
        "Truncate long cells to the \"min width\" set above.": "将长单元格截断为上面设置的\"最小宽度\"。",
        "Try different criteria to display results.": "尝试不同的条件以显示结果。",
        "Tukey": "Tukey",
        "Unable to calculate such a date delta": "无法计算这样的日期增量",
        "Unable to connect. Verify that the following roles are set on the service account: roles/bigquery.dataViewer, roles/bigquery.jobUser.": "无法连接。验证服务帐户上是否设置了以下角色：roles/bigquery.dataViewer、roles/bigquery.jobUser。",
        "Unable to create chart without a query id.": "无法在没有查询 ID 的情况下创建图表。",
        "Unable to decode value": "无法解码值",
        "Unable to encode value": "无法编码值",
        "Unable to load columns for the selected table. Please select a different table.": "无法加载所选表的列。请选择不同的表。",
        "Unable to parse SQL": "无法解析 SQL",
        "Unable to retrieve dashboard colors": "无法检索看板颜色",
        "Unable to sync permissions for this database connection.": "无法同步此数据库连接的权限。",
        "Upload a file with a valid extension. Valid: [%s]": "上传具有有效扩展名的文件。有效：[%s]",
        "Use \"%(menuName)s\" menu instead.": "请改用 \"%(menuName)s\" 菜单。",
        "Use date formatting even when metric value is not a timestamp.": "即使指标值不是时间戳，也使用日期格式。",
        "Use this section if you want a query that aggregates.": "如果您想要聚合查询，请使用此部分。",
        "Use this section if you want to query atomic rows.": "如果您想查询原子行，请使用此部分。",
        "User was successfully created!": "用户已成功创建！",
        "User was successfully updated!": "用户已成功更新！",
        "Validating connectivity for %s": "正在验证 %s 的连接性",
        "Value difference between the time periods": "时间段之间的值差异",
        "Value less than": "值小于",
        "Values selected in other filters will affect the filter options shown in this filter.": "在其他过滤器中选择的值将影响此过滤器中显示的过滤器选项。",
        "Visualize geospatial data like 3D buildings, landscapes, or anything else that can be represented by triangles.": "可视化地理空间数据，如 3D 建筑、景观或任何其他可以用三角形表示的内容。",
        "Visualizes connected points, which form a path, on a map.": "在地图上可视化形成路径的连接点。",
        "Visualizes geographic areas from your data as polygons on a map.": "将数据中的地理区域可视化为地图上的多边形。",
        "WFS": "WFS",
        "WMS": "WMS",
        "We have the following keys: %s": "我们有以下键：%s",
        "We were unable to carry over any controls when switching to this chart type.": "切换到此图表类型时，我们无法保留任何控件。",
        "Weekly Report for %s": "%s 的每周报告",
        "When unchecked, colors from the selected color scheme will be used.": "未选中时，将使用所选配色方案中的颜色。",
        "When using other than adaptive formatting, labels may overlap.": "使用自适应格式以外的格式时，标签可能会重叠。",
        "When using this option, default value can't be set. Using the time range from the URL or the default time range is recommended.": "使用此选项时，无法设置默认值。建议使用 URL 中的时间范围或默认时间范围。",
        "Write a handlebars template to render the data": "编写 handlebars 模板以渲染数据",
        "XYZ": "XYZ",
        "Year (freq=AS)": "年（频率=AS）",
        "You are viewing this chart in a dashboard context with label: %(label)s": "您正在查看标签为 %(label)s 的看板上下文中的此图表",
        "You are viewing this chart in the context of a dashboard that has time range filters applied.": "您正在查看应用了时间范围过滤器的看板上下文中的此图表。",
        "You can add the components in the": "您可以在",
        "You can add the components in the edit mode.": "您可以在编辑模式下添加组件。",
        "You can also just click on the chart to apply cross-filter.": "您也可以直接单击图表以应用交叉过滤器。",
        "You cannot delete the last temporal filter as it's used for time range filtering.": "您无法删除最后一个时间过滤器，因为它用于时间范围过滤。",
        # 继续补全剩余的翻译（带前导空格的版本）
        " at line %(line)d": "在第 %(line)d 行",
        "' at line %(line)d'": "在第 %(line)d 行",
        " near '%(highlight)s'": "在 '%(highlight)s' 附近",
        "\" near '%(highlight)s'\"": "在 '%(highlight)s' 附近",
        " source code of Superset's sandboxed parser": "Superset 沙箱解析器的源代码",
        "\" source code of Superset's sandboxed parser\"": "Superset 沙箱解析器的源代码",
        " to mark a column as a time column": "以将列标记为时间列",
        "' to mark a column as a time column'": "以将列标记为时间列",
        " to visualize your data.": "以可视化您的数据。",
        "' to visualize your data.'": "以可视化您的数据。",
        "%s items could not be tagged because you don't have edit permissions to all selected objects.": "%s 个项目无法标记，因为您没有对所有选定对象的编辑权限。",
        "Allow the execution of DDL (Data Definition Language: CREATE, DROP, TRUNCATE, etc.) and DML (Data Modification Language: INSERT, UPDATE, DELETE, etc)": "允许执行 DDL（数据定义语言：CREATE、DROP、TRUNCATE 等）和 DML（数据操作语言：INSERT、UPDATE、DELETE 等）",
        "Choose whether a country should be shaded by the metric, or assigned a color based on a categorical color palette": "选择国家是否应根据指标着色，或根据分类调色板分配颜色",
        "Color will be shaded based the normalized (0% to 100%) value of a given cell against the other cells in the selected range: ": "颜色将根据给定单元格相对于选定范围内其他单元格的标准化（0% 到 100%）值进行着色：",
        "'Color will be shaded based the normalized (0% to 100%) value of a given cell against the other cells in the selected range: '": "颜色将根据给定单元格相对于选定范围内其他单元格的标准化（0% 到 100%）值进行着色：",
        "Customize chart metrics or columns with currency symbols as prefixes or suffixes. Choose a symbol from dropdown or type your own.": "使用货币符号作为前缀或后缀自定义图表指标或列。从下拉菜单中选择符号或输入您自己的符号。",
        "Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: ": "可能未安装用于导入的数据库驱动程序。访问 Superset 文档页面查看安装说明：",
        "'Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: '": "可能未安装用于导入的数据库驱动程序。访问 Superset 文档页面查看安装说明：",
        "Define the database, SQL query, and triggering conditions for alert.": "定义警报的数据库、SQL 查询和触发条件。",
        "Defines the value that determines the boundary between different regions or levels in the data ": "定义确定数据中不同区域或级别之间边界的值",
        "'Defines the value that determines the boundary between different regions or levels in the data '": "定义确定数据中不同区域或级别之间边界的值",
        "Display percents in the label and tooltip as the percent of the total value, from the first step of the funnel, or from the previous step in the funnel.": "在标签和工具提示中将百分比显示为总值、漏斗第一步或漏斗上一步的百分比。",
        "Downloading %(rows)s rows based on the LIMIT configuration. If you want the entire result set, you need to adjust the LIMIT.": "根据 LIMIT 配置下载 %(rows)s 行。如果您想要整个结果集，需要调整 LIMIT。",
        "Go to the edit mode to configure the dashboard and add charts": "进入编辑模式以配置看板并添加图表",
        "If changes are made to your SQL query, columns in your dataset will be synced when saving the dataset.": "如果对 SQL 查询进行了更改，保存数据集时将同步数据集中的列。",
        "If enabled, this control sorts the results/values descending, otherwise it sorts the results ascending.": "如果启用，此控件将按降序对结果/值进行排序，否则按升序排序。",
        "In order to connect to non-public sheets you need to either provide a service account or configure an OAuth2 client.": "为了连接到非公共表格，您需要提供服务帐户或配置 OAuth2 客户端。",
        "Intensity is the value multiplied by the weight to obtain the final weight": "强度是值乘以权重以获得最终权重",
        "Minimum radius size of the circle, in pixels. As the zoom level changes, this insures that the circle respects this minimum radius.": "圆的最小半径大小（像素）。随着缩放级别的变化，这确保圆遵循此最小半径。",
        "Not all required fields are complete. Please provide the following:": "并非所有必填字段都已完成。请提供以下内容：",
        "Number of periods to compare against. You can use negative numbers to compare from the beginning of the time range.": "要比较的周期数。您可以使用负数从时间范围的开始进行比较。",
        "Opacity of bubbles, 0 means completely transparent, 1 means opaque": "气泡的不透明度，0 表示完全透明，1 表示不透明",
        "Orders the query result that generates the source data for this chart. If a series or row limit is reached, this determines what data are truncated. If undefined, defaults to the first metric (where appropriate).": "对生成此图表源数据的查询结果进行排序。如果达到系列或行限制，这将确定要截断的数据。如果未定义，则默认为第一个指标（在适当的情况下）。",
        "Overlays a hexagonal grid on a map, and aggregates data within the boundary of each cell.": "在地图上叠加六边形网格，并在每个单元格的边界内聚合数据。",
        "Pick a set of deck.gl charts to layer on top of one another": "选择一组 deck.gl 图表以相互叠加",
        "Please specify the Dataset ID for the ``%(name)s`` metric in the Jinja macro.": "请在 Jinja 宏中为 ``%(name)s`` 指标指定数据集 ID。",
        "Plot the distance (like flight paths) between origin and destination.": "绘制起点和终点之间的距离（如飞行路径）。",
        "Put positive values and valid minute and second value less than 60": "输入正值和小于 60 的有效分钟和秒值",
        "Renders table cells as HTML when applicable. For example, HTML <a> tags will be rendered as hyperlinks.": "在适用时将表格单元格渲染为 HTML。例如，HTML <a> 标签将渲染为超链接。",
        "Select a time grain for the visualization. The grain is the time interval represented by a single point on the chart.": "为可视化选择时间粒度。粒度是图表上单个点表示的时间间隔。",
        "Select columns that will be displayed in the table. You can multiselect columns.": "选择将在表中显示的列。您可以多选列。",
        "Select shape for computing values. \"FIXED\" sets all zoom levels to the same size. \"LINEAR\" increases sizes linearly based on specified slope. \"EXP\" increases sizes exponentially based on specified exponent": "选择用于计算值的形状。\"FIXED\" 将所有缩放级别设置为相同大小。\"LINEAR\" 根据指定的斜率线性增加大小。\"EXP\" 根据指定的指数指数增加大小",
        "Something went wrong with embedded authentication. Check the dev console for details.": "嵌入式身份验证出现问题。查看开发控制台以了解更多详细信息。",
        "Syntax Error: %(qualifier)s input \"%(input)s\" expecting \"%(expected)s": "语法错误：%(qualifier)s 输入 \"%(input)s\" 期望 \"%(expected)s\"",
        "Table already exists. You can change your 'if table already exists' strategy to append or replace or provide a different Table Name to use.": "表已存在。您可以将\"如果表已存在\"策略更改为追加或替换，或提供不同的表名。",
        "The GeoJsonLayer takes in GeoJSON formatted data and renders it as interactive polygons, lines and points (circles, icons and/or texts).": "GeoJsonLayer 接收 GeoJSON 格式的数据并将其渲染为交互式多边形、线条和点（圆形、图标和/或文本）。",
        "The dataset column/metric that returns the values on your chart's x-axis.": "返回图表 x 轴上值的数据集列/指标。",
        "The dataset column/metric that returns the values on your chart's y-axis.": "返回图表 y 轴上值的数据集列/指标。",
        "The extent of the map on application start. FIT DATA automatically sets the extent so that all data points are included in the viewport. CUSTOM allows users to define the extent manually.": "应用程序启动时地图的范围。FIT DATA 自动设置范围，以便所有数据点都包含在视口中。CUSTOM 允许用户手动定义范围。",
        "The function to use when aggregating points into groups": "将点聚合为组时使用的函数",
        "The height of the current zoom level to compute all heights from": "用于计算所有高度的当前缩放级别的高度",
        "The result of this query must be a value capable of numeric interpretation e.g. 1, 1.0, or \"1\" (compatible with Python's float() function).": "此查询的结果必须是能够进行数字解释的值，例如 1、1.0 或 \"1\"（与 Python 的 float() 函数兼容）。",
        "The row limit set for the chart was reached. The chart may show partial data.": "已达到为图表设置的行限制。图表可能显示部分数据。",
        "The user/password combination is not valid (Incorrect password for user).": "用户/密码组合无效（用户密码不正确）。",
        "The width of the current zoom level to compute all widths from": "用于计算所有宽度的当前缩放级别的宽度",
        "This chart is managed externally, and can't be edited in Superset": "此图表由外部管理，无法在 Superset 中编辑",
        "This chart type is not supported when using an unsaved query as a chart source. ": "使用未保存的查询作为图表源时不支持此图表类型。",
        "'This chart type is not supported when using an unsaved query as a chart source. '": "使用未保存的查询作为图表源时不支持此图表类型。",
        "This control filters the whole chart based on the selected time range. All relative times, e.g. \"Last month\", \"Last 7 days\", \"now\", etc. are evaluated on the server using the server's local time (sans timezone). All tooltips and placeholder times are expressed in UTC (sans timezone). The timestamps are then evaluated by the database using the engine's local timezone. Note one can explicitly set the timezone per the ISO 8601 format if specifying either the start and/or end time.": "此控件根据所选时间范围过滤整个图表。所有相对时间，例如\"上个月\"、\"过去 7 天\"、\"现在\"等，都使用服务器的本地时间（无时区）在服务器上评估。所有工具提示和占位符时间都以 UTC（无时区）表示。然后，数据库使用引擎的本地时区评估时间戳。请注意，如果指定开始时间和/或结束时间，可以按照 ISO 8601 格式显式设置时区。",
        "This dashboard is managed externally, and can't be edited in Superset": "此看板由外部管理，无法在 Superset 中编辑",
        "This database does not allow for DDL/DML, and the query could not be parsed to confirm it is a read-only query. Please contact your administrator for more assistance.": "此数据库不允许 DDL/DML，无法解析查询以确认它是只读查询。请联系您的管理员以获得更多帮助。",
        "This database is managed externally, and can't be edited in Superset": "此数据库由外部管理，无法在 Superset 中编辑",
        "This database table does not contain any data. Please select a different table.": "此数据库表不包含任何数据。请选择不同的表。",
        "This dataset is managed externally, and can't be edited in Superset": "此数据集由外部管理，无法在 Superset 中编辑",
        "This field is used as a unique identifier to attach the calculated dimension to charts. It is also used as the alias in the SQL query.": "此字段用作唯一标识符，用于将计算的维度附加到图表。它也用作 SQL 查询中的别名。",
        "This field is used as a unique identifier to attach the metric to charts. It is also used as the alias in the SQL query.": "此字段用作唯一标识符，用于将指标附加到图表。它也用作 SQL 查询中的别名。",
        "This page is intended to be embedded in an iframe, but it looks like that is not the case.": "此页面旨在嵌入在 iframe 中，但看起来情况并非如此。",
        "This session has encountered an interruption, and some controls may not work as intended. If you are the developer of this app, please check that the guest token is being generated correctly.": "此会话遇到中断，某些控件可能无法按预期工作。如果您是此应用程序的开发人员，请检查访客令牌是否正在正确生成。",
        "This will be applied to the whole table. Arrows (↑ and ↓) will be added to main columns for increase and decrease. Basic conditional formatting can be overwritten by conditional formatting below.": "这将应用于整个表格。箭头（↑ 和 ↓）将添加到主列以表示增加和减少。基本条件格式可以被下面的条件格式覆盖。",
        "To enable multiple column sorting, hold down the ⇧ Shift key while clicking the column header.": "要启用多列排序，请在单击列标题时按住 ⇧ Shift 键。",
        "Truncate long cells to the \"min width\" set above": "将长单元格截断为上面设置的\"最小宽度\"",
        "Unable to connect. Verify that the following roles are set on the service account: \"BigQuery Data Viewer\", \"BigQuery Metadata Viewer\", \"BigQuery Job User\" and the following permissions are set \"bigquery.readsessions.create\", \"bigquery.readsessions.getData\"": "无法连接。验证服务帐户上是否设置了以下角色：\"BigQuery 数据查看器\"、\"BigQuery 元数据查看器\"、\"BigQuery 作业用户\"，以及是否设置了以下权限 \"bigquery.readsessions.create\"、\"bigquery.readsessions.getData\"",
        "Use date formatting even when metric value is not a timestamp": "即使指标值不是时间戳，也使用日期格式",
        "Use this section if you want a query that aggregates": "如果您想要聚合查询，请使用此部分",
        "Use this section if you want to query atomic rows": "如果您想查询原子行，请使用此部分",
        "Values selected in other filters will affect the filter options to only show relevant values": "在其他过滤器中选择的值将影响过滤器选项，仅显示相关值",
        "Visualize geospatial data like 3D buildings, landscapes, or objects in grid view.": "在网格视图中可视化地理空间数据，如 3D 建筑、景观或对象。",
        "Visualizes geographic areas from your data as polygons on a Mapbox rendered map. Polygons can be colored using a metric.": "将数据中的地理区域可视化为 Mapbox 渲染地图上的多边形。可以使用指标为多边形着色。",
        "We were unable to carry over any controls when switching to this new dataset.": "切换到此新数据集时，我们无法保留任何控件。",
        "When unchecked, colors from the selected color scheme will be used for time shifted series": "未选中时，所选配色方案中的颜色将用于时间偏移系列",
        "When using other than adaptive formatting, labels may overlap": "使用自适应格式以外的格式时，标签可能会重叠",
        "When using this option, default value can't be set. Using this option may impact the load times for your dashboard.": "使用此选项时，无法设置默认值。使用此选项可能会影响看板的加载时间。",
        "'When using this option, default value can't be set. Using this option may impact the load times for your dashboard.'": "使用此选项时，无法设置默认值。使用此选项可能会影响看板的加载时间。",
        "You cannot delete the last temporal filter as it's used for time range filters in dashboards.": "您无法删除最后一个时间过滤器，因为它用于看板中的时间范围过滤器。",
        "You have used all %(historyLength)s undo slots and will not be able to fully undo subsequent actions. You may save your current state to reset the history.": "您已使用所有 %(historyLength)s 个撤销槽，将无法完全撤销后续操作。您可以保存当前状态以重置历史记录。",
        "You may have an error in your SQL statement. {message}": "您的 SQL 语句可能有错误。{message}",
        "You must be a dataset owner in order to edit. Please reach out to a dataset owner to request modifications or edit access.": "您必须是数据集所有者才能编辑。请联系数据集所有者以请求修改或编辑访问权限。",
        "You've changed datasets. Any controls with data (columns, metrics) that match this new dataset have been retained.": "您已更改数据集。与此新数据集匹配的任何数据（列、指标）控件都已保留。",
        "Your dashboard is near the size limit.": "您的看板接近大小限制。",
        "Your range is not within the dataset range": "您的范围不在数据集范围内",
        "ZIP file contains multiple file types": "ZIP 文件包含多种文件类型",
        "Add colors to cell bars for +/-": "为 +/- 的单元格条添加颜色",
        "asfreq": "asfreq",
        "between {down} and {up} {name}": "在 {down} 和 {up} 之间 {name}",
        "bfill": "bfill",
        "boolean type icon": "布尔类型图标",
        "code ISO 3166-1 alpha-2 (cca2)": "代码 ISO 3166-1 alpha-2 (cca2)",
        "code ISO 3166-1 alpha-3 (cca3)": "代码 ISO 3166-1 alpha-3 (cca3)",
        "code International Olympic Committee (cioc)": "代码国际奥林匹克委员会 (cioc)",
        "connecting to %(dbModelName)s": "正在连接到 %(dbModelName)s",
        "dialect+driver://username:password@host:port/database": "dialect+driver://username:password@host:port/database",
        "e.g. hive_metastore": "例如 hive_metastore",
        "ffill": "ffill",
        "function type icon": "函数类型图标",
        "geohash (square)": "geohash（方形）",
        "is not": "不是",
        "less than {min} {name}": "小于 {min} {name}",
        "more than {max} {name}": "大于 {max} {name}",
        "numeric type icon": "数字类型图标",
        "p1": "p1",
        "p5": "p5",
        "p95": "p95",
        "p99": "p99",
        "page_size.all": "page_size.all",
        "restore zoom": "恢复缩放",
        "sql": "sql",
        "x": "x",
        "x: values are normalized within each column": "x：值在每个列内标准化",
        "y": "y",
        "y: values are normalized within each row": "y：值在每一行内标准化",
        "© Layer attribution": "© 图层归属",
    }
    
    # Check if we have a direct translation (try both original and cleaned)
    if msgid_original in translations:
        return translations[msgid_original]
    if msgid_clean in translations:
        return translations[msgid_clean]
    
    # For multi-line strings, try to translate each line
    if '\n' in msgid_clean:
        lines = msgid_clean.split('\n')
        translated_lines = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped in translations:
                translated_lines.append(translations[line_stripped])
            elif line_stripped:
                # Keep original if no translation found
                translated_lines.append(line)
            else:
                translated_lines.append('')
        return '\n'.join(translated_lines)
    
    # Return empty string to indicate no translation available
    return ""


def complete_translations():
    """Complete missing translations in the PO file."""
    if not PO_FILE.exists():
        print(f"Error: {PO_FILE} not found")
        sys.exit(1)
    
    print(f"Reading {PO_FILE}...")
    
    # Read the PO file
    with open(PO_FILE, 'rb') as f:
        catalog_obj = pofile.read_po(f)
    
    total_entries = len(catalog_obj)
    untranslated_count = 0
    translated_count = 0
    
    print(f"Total entries: {total_entries}")
    
    # Process each message
    for message in catalog_obj:
        # Skip empty msgid (header)
        if not message.id:
            continue
        
        # Check if translation is missing
        if not message.string or message.string == "":
            untranslated_count += 1
            translation = translate_string(message.id)
            
            if translation:
                message.string = translation
                # Remove fuzzy flag if present
                if 'fuzzy' in message.flags:
                    message.flags.remove('fuzzy')
                translated_count += 1
                print(f"✓ Translated: {message.id[:60]}...")
            else:
                print(f"✗ No translation available: {message.id[:60]}...")
    
    print(f"\nSummary:")
    print(f"  Untranslated entries: {untranslated_count}")
    print(f"  Auto-translated: {translated_count}")
    print(f"  Remaining: {untranslated_count - translated_count}")
    
    # Write back to file
    if translated_count > 0:
        print(f"\nWriting updated translations to {PO_FILE}...")
        with open(PO_FILE, 'wb') as f:
            pofile.write_po(f, catalog_obj, width=79)
        print("✓ File updated successfully!")
    else:
        print("\nNo translations were added. File not modified.")


if __name__ == "__main__":
    complete_translations()
