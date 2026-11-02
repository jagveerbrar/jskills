#!/usr/bin/env bash
set -euo pipefail

# Directories
HUB_DIR="${HOME}/.agents/skills"
JSKILLS_DIR="${HOME}/Projects/jskills"
JSKILLS_PRIVATE_DIR="${HOME}/Projects/jskills-private"
EXTERNAL_DIR="${HOME}/Projects/external-skills"

ACTION="sync"
if [ "${1:-}" = "--pull" ] || [ "${1:-}" = "-p" ]; then
    ACTION="pull"
elif [ "${1:-}" = "--check" ] || [ "${1:-}" = "-c" ]; then
    ACTION="check"
fi

mkdir -p "${HUB_DIR}"
mkdir -p "${EXTERNAL_DIR}"

# 1. Handle Upstream Git Operations
if [ "${ACTION}" = "pull" ]; then
    echo "=================================================="
    echo " Pulling Latest Upstream Updates"
    echo "=================================================="
    if [ -d "${EXTERNAL_DIR}" ]; then
        for repo in "${EXTERNAL_DIR}"/*/; do
            if [ -d "${repo}/.git" ]; then
                repo_name=$(basename "${repo}")
                echo "--> Updating ${repo_name}..."
                git -C "${repo}" pull --ff-only || echo "  [warning] Failed to fast-forward ${repo_name}"
            fi
        done
    fi
elif [ "${ACTION}" = "check" ]; then
    echo "=================================================="
    echo " Checking Upstream Repositories for Updates"
    echo "=================================================="
    has_updates=0
    if [ -d "${EXTERNAL_DIR}" ]; then
        for repo in "${EXTERNAL_DIR}"/*/; do
            if [ -d "${repo}/.git" ]; then
                repo_name=$(basename "${repo}")
                git -C "${repo}" fetch --quiet
                behind=$(git -C "${repo}" rev-list HEAD..@{u} --count 2>/dev/null || echo "0")
                if [ "${behind}" -gt 0 ]; then
                    echo "  [UPDATE AVAILABLE] ${repo_name} is ${behind} commit(s) behind upstream."
                    has_updates=1
                else
                    echo "  [UP TO DATE] ${repo_name}"
                fi
            fi
        done
    fi
    if [ "${has_updates}" -eq 0 ]; then
        echo "All external repositories are up to date."
    else
        echo ""
        echo "Run '$0 --pull' to apply updates."
    fi
    exit 0
fi

# 2. Main Sync Routine
echo ""
echo "=================================================="
echo " Synchronizing Agent Skills to ${HUB_DIR}"
echo "=================================================="

# Prune broken symlinks
echo "--> Auditing existing symlinks..."
pruned_count=0
for link in "${HUB_DIR}"/*; do
    if [ -L "${link}" ] && [ ! -e "${link}" ]; then
        echo "  [pruned broken link] $(basename "${link}")"
        rm "${link}"
        pruned_count=$((pruned_count + 1))
    fi
done
if [ "${pruned_count}" -eq 0 ]; then
    echo "  No broken symlinks found."
fi

# 1. Link private skills from jskills-private (highest precedence)
private_count=0
if [ -d "${JSKILLS_PRIVATE_DIR}" ]; then
    echo ""
    echo "--> Linking private skills from ${JSKILLS_PRIVATE_DIR}..."
    for skill_dir in "${JSKILLS_PRIVATE_DIR}"/*/; do
        [ -d "${skill_dir}" ] || continue
        skill_dir="${skill_dir%/}"
        skill_name=$(basename "${skill_dir}")
        
        case "${skill_name}" in
            scripts|references|scratch|evals|node_modules|.git|.github)
                continue
                ;;
        esac

        if [ -f "${skill_dir}/SKILL.md" ]; then
            ln -sfn "${skill_dir}" "${HUB_DIR}/${skill_name}"
            echo "  [private] ${skill_name} -> ${skill_dir}"
            private_count=$((private_count + 1))
        fi
    done
fi

# 2. Link public custom skills from jskills
echo ""
echo "--> Linking public custom skills from ${JSKILLS_DIR}..."
public_count=0
for skill_dir in "${JSKILLS_DIR}"/*/; do
    [ -d "${skill_dir}" ] || continue
    skill_dir="${skill_dir%/}"
    skill_name=$(basename "${skill_dir}")
    
    case "${skill_name}" in
        scripts|references|scratch|evals|node_modules|.git|.github)
            continue
            ;;
    esac

    if [ -f "${skill_dir}/SKILL.md" ]; then
        if [ -d "${JSKILLS_PRIVATE_DIR}/${skill_name}" ] && [ -f "${JSKILLS_PRIVATE_DIR}/${skill_name}/SKILL.md" ]; then
            echo "  [override] ${skill_name} (using private jskills-private version)"
            continue
        fi
        ln -sfn "${skill_dir}" "${HUB_DIR}/${skill_name}"
        echo "  [public] ${skill_name} -> ${skill_dir}"
        public_count=$((public_count + 1))
    fi
done

# 3. Link external skills
echo ""
echo "--> Linking external skills from ${EXTERNAL_DIR}..."
external_count=0
skipped_count=0

if [ -d "${EXTERNAL_DIR}" ]; then
    while IFS= read -r skill_file; do
        [ -z "${skill_file}" ] && continue
        skill_dir=$(dirname "${skill_file}")
        skill_name=$(basename "${skill_dir}")

        if [ -d "${JSKILLS_PRIVATE_DIR}/${skill_name}" ] && [ -f "${JSKILLS_PRIVATE_DIR}/${skill_name}/SKILL.md" ]; then
            echo "  [override] ${skill_name} (using private jskills-private version)"
            skipped_count=$((skipped_count + 1))
        elif [ -d "${JSKILLS_DIR}/${skill_name}" ] && [ -f "${JSKILLS_DIR}/${skill_name}/SKILL.md" ]; then
            echo "  [override] ${skill_name} (using custom jskills version)"
            skipped_count=$((skipped_count + 1))
        else
            ln -sfn "${skill_dir}" "${HUB_DIR}/${skill_name}"
            echo "  [external] ${skill_name} -> ${skill_dir}"
            external_count=$((external_count + 1))
        fi
    done < <(find "${EXTERNAL_DIR}" -maxdepth 4 -type f -name "SKILL.md" 2>/dev/null || true)
fi

echo ""
echo "=================================================="
echo " Summary: ${public_count} public, ${private_count} private, ${external_count} external active in ${HUB_DIR}"
echo "=================================================="
