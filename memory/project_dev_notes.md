# Project Development Notes

> 开发文档、决策记录和技术债务追踪

---

## 1. 设计决策记录

### 决策 1：项目配置文件格式

**日期**：2026-05-28

**背景**：
- 需要一个标准化的项目配置格式
- 考虑了 YAML、TOML、JSON 三种格式

**决策**：
- 选择 JSON 格式

**理由**：
1. **广泛支持**：所有语言都有 JSON 解析器
2. **工具链成熟**：`jq` 等工具可以轻松处理
3. **严格性**：JSON 语法严格，减少配置错误
4. **可扩展性**：支持嵌套结构

**替代方案**：
- YAML：更易读，但语法宽松容易出错
- TOML：适合配置文件，但工具链不如 JSON 成熟

**影响**：
- 所有项目使用 `.gaproject` JSON 文件
- 需要提供 JSON schema 验证

---

### 决策 2：docs branch 永不合并

**日期**：2026-05-28

**背景**：
- 需要追踪项目的设计决策和演化历史
- 考虑了多种方案：单独仓库、子目录、独立分支

**决策**：
- 使用独立的 `docs` branch，永不合并到 `main`

**理由**：
1. **清晰分离**：代码和文档完全分离，互不干扰
2. **独立演化**：docs branch 可以有自己的提交历史
3. **避免冲突**：永不合并，不会产生合并冲突
4. **灵活性**：可以随时切换查看文档

**替代方案**：
- 单独仓库：管理复杂，需要同步两个仓库
- 子目录（如 `docs/`）：会污染代码仓库，增加代码审查负担

**影响**：
- 所有项目必须创建 `docs` branch
- 文档更新使用 `git checkout docs`
- 需要教育用户"永不合并"的原则

---

### 决策 3：临时文件统一管理

**日期**：2026-05-28

**背景**：
- 临时文件散落在项目各处，难以清理
- 需要一个统一的临时文件管理机制

**决策**：
- 所有临时文件放在 `.ga_temp/` 目录

**理由**：
1. **集中管理**：一个目录包含所有临时文件
2. **易于清理**：`rm -rf .ga_temp/` 即可清理
3. **Git 友好**：添加到 `.gitignore` 即可忽略
4. **结构化**：可以在 `.ga_temp/` 下创建子目录（sessions/, cache/, logs/）

**替代方案**：
- 系统临时目录（`/tmp/`）：跨项目共享，难以隔离
- 项目根目录：污染项目结构

**影响**：
- 所有项目必须创建 `.ga_temp/` 目录
- `.ga_temp/` 必须添加到 `.gitignore`
- 工具调用需要适配（临时文件路径）

---

### 决策 4：项目发现机制

**日期**：2026-05-29

**背景**：
- 用户可能在项目的任意子目录中启动 GA
- 需要自动发现项目根目录

**决策**：
- 从当前目录向上查找，直到找到 `.gaproject` 或 `.git/`

**理由**：
1. **用户友好**：无需手动指定项目根目录
2. **灵活性**：支持在子目录中工作
3. **标准化**：与 Git 的行为一致

**替代方案**：
- 要求用户手动指定：不够友好
- 只在当前目录查找：不够灵活

**影响**：
- 项目发现逻辑需要实现向上查找
- 需要处理未找到项目的情况

---

### 决策 5：配置优先级

**日期**：2026-05-29

**背景**：
- 用户可能有全局配置和项目配置
- 需要明确优先级

**决策**：
- 项目配置 > 全局配置 > 默认值

**理由**：
1. **就近原则**：项目配置最接近用户意图
2. **灵活性**：可以为特定项目定制配置
3. **一致性**：与大多数工具的行为一致

**影响**：
- 配置加载逻辑需要实现优先级
- 需要文档说明优先级规则

---

## 2. 技术债务

### 债务 1：项目列表持久化

**状态**：🔴 未实现

**描述**：
- 当前项目列表只在内存中，重启后丢失
- 需要持久化到文件（如 `~/.config/ga/projects.json`）

**影响**：
- 用户需要重新发现项目
- `ga project list` 无法显示历史项目

**优先级**：P1（高）

**预计工作量**：2 小时

---

### 债务 2：项目模板系统

**状态**：🟡 部分实现

**描述**：
- 当前只有基本的项目类型检测
- 需要完整的模板系统（Python/Node.js/Rust/Go 等）

**影响**：
- 用户需要手动配置项目
- 无法快速创建标准化项目

**优先级**：P2（中）

**预计工作量**：1 天

---

### 债务 3：项目健康检查

**状态**：🔴 未实现

**描述**：
- 需要定期检查项目健康度（测试覆盖率、代码质量、文档完整性等）
- 可以集成 waza health

**影响**：
- 无法自动发现项目问题
- 技术债务积累

**优先级**：P3（低）

**预计工作量**：3 天

---

### 债务 4：跨项目依赖追踪

**状态**：🔴 未实现

**描述**：
- 当前无法追踪项目之间的依赖关系
- 需要在 `.gaproject` 中声明依赖

**影响**：
- Monorepo 支持不完整
- 无法自动加载依赖项目的上下文

**优先级**：P3（低）

**预计工作量**：2 天

---

## 3. 未来规划

### 3.1 短期（1-2 周）

- [ ] 实现项目列表持久化
- [ ] 完善项目模板系统
- [ ] 添加项目配置验证（JSON schema）
- [ ] 改进错误提示（配置错误、路径错误等）

### 3.2 中期（1-2 月）

- [ ] 实现项目健康检查
- [ ] 支持跨项目依赖追踪
- [ ] 添加项目迁移工具（从其他工具迁移到 GA）
- [ ] 支持项目模板市场（社区贡献模板）

### 3.3 长期（3-6 月）

- [ ] 支持远程项目（SSH、容器等）
- [ ] 支持项目协作（多人同时工作）
- [ ] 集成更多工具（Docker、Kubernetes 等）
- [ ] 支持项目分析和可视化

---

## 4. 实现细节

### 4.1 项目发现算法

```python
def discover_project(start_dir: Path) -> Optional[Path]:
    """
    从 start_dir 向上查找项目根目录
    
    查找顺序：
    1. .gaproject 文件（最高优先级）
    2. .git/ 目录
    3. 项目配置文件（package.json, pyproject.toml 等）
    4. IDE 配置目录（.vscode/, .idea/）
    """
    current = start_dir
    while current != current.parent:  # 直到根目录
        # 1. 检查 .gaproject
        if (current / '.gaproject').exists():
            return current
        
        # 2. 检查 .git/
        if (current / '.git').is_dir():
            return current
        
        # 3. 检查项目配置文件
        for config_file in ['package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod']:
            if (current / config_file).exists():
                return current
        
        # 4. 检查 IDE 配置目录
        for ide_dir in ['.vscode', '.idea']:
            if (current / ide_dir).is_dir():
                return current
        
        current = current.parent
    
    return None
```

### 4.2 配置加载逻辑

```python
def load_config(project_root: Path) -> dict:
    """
    加载项目配置，处理优先级
    
    优先级：项目配置 > 全局配置 > 默认值
    """
    # 1. 默认值
    config = {
        'version': '1.0',
        'project_name': project_root.name,
        'project_root': '.',
        'temp_dir': '.ga_temp',
        'ignore_patterns': ['.git/', '.ga_temp/', '__pycache__/'],
        'context_files': [],
        'custom_prompt': ''
    }
    
    # 2. 全局配置
    global_config_path = Path.home() / '.config' / 'ga' / 'config.json'
    if global_config_path.exists():
        with open(global_config_path) as f:
            global_config = json.load(f)
            config.update(global_config)
    
    # 3. 项目配置
    project_config_path = project_root / '.gaproject'
    if project_config_path.exists():
        with open(project_config_path) as f:
            project_config = json.load(f)
            config.update(project_config)
    
    return config
```

### 4.3 临时文件管理

```python
class TempFileManager:
    """临时文件管理器"""
    
    def __init__(self, project_root: Path, temp_dir: str = '.ga_temp'):
        self.project_root = project_root
        self.temp_dir = project_root / temp_dir
        self.temp_dir.mkdir(exist_ok=True)
    
    def get_session_dir(self, session_id: str) -> Path:
        """获取 session 级临时目录"""
        session_dir = self.temp_dir / 'sessions' / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir
    
    def get_cache_dir(self) -> Path:
        """获取缓存目录"""
        cache_dir = self.temp_dir / 'cache'
        cache_dir.mkdir(exist_ok=True)
        return cache_dir
    
    def get_log_dir(self) -> Path:
        """获取日志目录"""
        log_dir = self.temp_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        return log_dir
    
    def clean(self):
        """清理所有临时文件"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir()
```

---

## 5. 测试策略

### 5.1 单元测试

```python
# tests/test_project_discovery.py
def test_discover_project_with_gaproject():
    """测试：发现包含 .gaproject 的项目"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir) / 'my-project'
        project_root.mkdir()
        (project_root / '.gaproject').write_text('{}')
        
        # 从子目录发现
        subdir = project_root / 'src' / 'utils'
        subdir.mkdir(parents=True)
        
        discovered = discover_project(subdir)
        assert discovered == project_root

def test_discover_project_with_git():
    """测试：发现包含 .git/ 的项目"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir) / 'my-project'
        project_root.mkdir()
        (project_root / '.git').mkdir()
        
        discovered = discover_project(project_root)
        assert discovered == project_root
```

### 5.2 集成测试

```python
# tests/test_project_lifecycle.py
def test_full_lifecycle():
    """测试：完整的项目生命周期"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. 创建项目
        project_root = Path(tmpdir) / 'my-project'
        init_project(project_root, template='python')
        
        # 2. 验证文件结构
        assert (project_root / '.gaproject').exists()
        assert (project_root / '.ga_temp').is_dir()
        assert (project_root / '.git').is_dir()
        
        # 3. 加载项目
        config = load_config(project_root)
        assert config['project_name'] == 'my-project'
        
        # 4. 清理临时文件
        temp_manager = TempFileManager(project_root)
        temp_manager.clean()
        assert not list((project_root / '.ga_temp').iterdir())
```

---

## 6. 性能优化

### 6.1 项目发现缓存

```python
# 缓存最近发现的项目，避免重复查找
_project_cache: Dict[Path, Path] = {}

def discover_project_cached(start_dir: Path) -> Optional[Path]:
    if start_dir in _project_cache:
        return _project_cache[start_dir]
    
    project_root = discover_project(start_dir)
    _project_cache[start_dir] = project_root
    return project_root
```

### 6.2 配置文件监听

```python
# 监听 .gaproject 变化，自动重新加载
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.gaproject'):
            reload_config()
```

---

**返回**：[← Project Lifecycle SOP](project_lifecycle_sop.md)

**版本**：v1.0  
**最后更新**：2026-05-30
